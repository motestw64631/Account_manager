import uvicorn
from fastapi import FastAPI, Request, status
from app.user.schemas import UserCreate, UserVerify, ResponseModel, ErrorResponse
from app.user import crud
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Depends
from datetime import datetime, timedelta
from functools import wraps
import traceback
import redis

app = FastAPI()
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
         loc = ".".join(error["loc"])
         msg = f"{loc}: {error['msg']}"
         errors.append(msg)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
               "success":False,
               "reason": errors[0]
               }),
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({
               "success":False,
               "reason": "Oops! Something Went Wrong"
               })
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(ErrorResponse(success=False, reason=exc.detail))
    )


password_failures = {}

def attempt_limiter(endpoint):
    @wraps(endpoint)
    async def wrapper(request: Request, *args, **kwargs):
        LOCKOUT_DURATION = timedelta(minutes=1)
        # Get the client's IP address
        client_ip = request.client.host

        # Create a storage key for each user
        user_key = f"rate_limit_{client_ip}"

        # Get the current time
        current_datetime = datetime.now()

        # Attempt to retrieve the failure attempts for the user
        failure_data = redis_client.hgetall(user_key)
        if not failure_data:
            # Initialize failure data if not present
            redis_client.hmset(user_key, {"attempts": 1, "lockout_time": ""})
        failure_data = redis_client.hgetall(user_key)
        if int(failure_data["attempts"]) >= 5:
            # If there are 5 or more failure attempts
            if not failure_data["lockout_time"]:
                # Set lockout_time when attempts first time > 5
                redis_client.hmset(user_key, {"attempts": 5, "lockout_time": (current_datetime + LOCKOUT_DURATION).timestamp()})
            elif current_datetime >= datetime.fromtimestamp(float(failure_data["lockout_time"])):
                # Remove limit when user wait > 1 min
                redis_client.hmset(user_key, {"attempts": 1, "lockout_time": ""})
            else:
                raise HTTPException(status_code=429, detail=f"Too many password verification failures. Please wait until {datetime.fromtimestamp(float(failure_data['lockout_time']))} before trying again.")

        # Increment attempts
        redis_client.hincrby(user_key, "attempts", 1)

        return endpoint(request, *args, **kwargs)

    return wrapper


@app.post("/users", response_model=ResponseModel, responses={
    400: {"model": ErrorResponse},
    422: {"model": ErrorResponse}
})
def create_user(user:UserCreate, db: Session = Depends(get_db)):
   db_user = crud.get_user_by_username(db, username=user.username)
   if db_user:
      return JSONResponse(status_code=400, content={"success": False, "reason": "username already registered"})
   created_user = crud.create_user(db=db, user=user)
   return JSONResponse(status_code=200, content={"success": True})
   
   
@app.post("/verify", response_model=ResponseModel, responses={
    401: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
    429: {"model": ErrorResponse}
})
@attempt_limiter
def verify_user(request: Request, user:UserVerify, db: Session = Depends(get_db)):
   verify = crud.verify_user(db=db, user=user)
   if verify['success']:
      return JSONResponse(status_code=200, content={"success": True})
   return JSONResponse(status_code=401, content={"success":False, "reason":verify["reason"]})




if __name__=="__main__":
    uvicorn.run("app.main:app",host='0.0.0.0', port=8087, reload=True, workers=1)



