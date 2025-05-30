from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="User already exists"


class IncorrectUserEmailOrPasswordException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Incorrect email or password"


class TokenExpiredException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Token expired"


class TokenAbsentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Token absent"


class IncorrectTokenFormatException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Incorrect token format"


class UserIsNotPresentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED


class RoomCanNotBeBookedException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Room can't be booked"


class NotAvailableHotelsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Not available hotels"


class NotAvailableRoomsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Not available rooms"

class NotBookingsException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Not bookings"

class RoomCanNotBeBookedIncorrectDaysException(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Room can't be booked, because you write incorrect days"

class NotHotelsIncorrectDaysException(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Not available hotels, because you write incorrect days"

class NotRoomsIncorrectDaysException(BookingException):
    status_code=status.HTTP_400_BAD_REQUEST
    detail="Not available rooms, because you write incorrect days"