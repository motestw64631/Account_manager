import uvicorn
from fastapi import FastAPI, Request, status
from app.user.schemas import UserCreate, UserVerify
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

app = FastAPI()


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



password_failures = {}

def attempt_limiter(endpoint):
    @wraps(endpoint)
    async def wrapper(request: Request, *args, **kwargs):
        global password_failures
        LOCKOUT_DURATION = timedelta(minutes=1)
        # Get the client's IP address
        client_ip = request.client.host

        # Create a storage key for each user
        user_key = f"rate_limit_{client_ip}"

        # Get the current time
        current_datetime = datetime.now()

        # Attempt to retrieve the failure attempts for the user
        failure_data = password_failures.get(user_key, None)
        if not failure_data:
            password_failures[user_key] = {"attempts": 1, "lockout_time": None}
        failure_data = password_failures[user_key]

        if failure_data["attempts"] >= 5:
            # If there are 5 or more failure attempts
            if failure_data["lockout_time"] is None:
                # Set lockout_time when attempts firt time > 5
                password_failures[user_key] = {"attempts": 5, "lockout_time": current_datetime + LOCKOUT_DURATION}
                # Remove limit when user wait > 1 min
            elif current_datetime >= failure_data["lockout_time"]:
                password_failures[user_key] = {"attempts": 1, "lockout_time": None}
            else:
                # Raise Exception
                raise HTTPException(status_code=429, detail=f"Too many password verification failures. Please wait until {failure_data['lockout_time']} before trying again.")

        # Increment attempts
        failure_data["attempts"] += 1

        return endpoint(request, *args, **kwargs)

    return wrapper


@app.post("/users")
def create_user(user:UserCreate, db: Session = Depends(get_db)):
   db_user = crud.get_user_by_username(db, username=user.username)
   if db_user:
      return JSONResponse(status_code=400, content={"success": False, "reason": "username already registered"})
   created_user = crud.create_user(db=db, user=user)
   return JSONResponse(status_code=200, content={"success": True})
   
   
@app.post("/verify")
@attempt_limiter
def verify_user(request: Request, user:UserVerify, db: Session = Depends(get_db)):
   verify = crud.verify_user(db=db, user=user)
   if verify['success']:
      return JSONResponse(status_code=200, content={"success": True})
   return JSONResponse(status_code=401, content={"success":False, "reason":verify["reason"]})




if __name__=="__main__":
    uvicorn.run("app.main:app",host='0.0.0.0', port=8087, reload=True, workers=1)



