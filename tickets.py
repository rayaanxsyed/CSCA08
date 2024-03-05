YR = 0      # year in format YYYY
MON = 4     # month in format MM
DAY = 6     # day in format DD
DEP = 8     # departure airport code: 3 letters
ARR = 11    # arrival airport code: 3 letters
ROW = 14    # row number: 2 digits
SEAT = 16   # seat: 1 letter
FFN = 17    # frequent flyer number: 4 digits

# seats
SA = 'A'
SB = 'B'
SC = 'C'
SD = 'D'
SE = 'E'
SF = 'F'

# seat types
WINDOW = 'window'
AISLE = 'aisle'
MIDDLE = 'middle'

def get_date(ticket: str) -> str:
    """Return the date of ticket 'ticket' in YYYYMMDD format.
    
    >>> get_date('20230915YYZYEG12F')
    '20230915'
    >>> get_date('20240915YYZYEG12F1236')
    '20240915'
    """      
    return get_year(ticket) + get_month(ticket) + get_day(ticket)

def get_year(ticket: str) -> str: 
    """Return the year of ticket 'ticket' in YYYY.
    
    >>> get_year('20230915YYZYEG12F')
    '2023'
    >>> get_year('20240915YYZYEG12F1236')
    '2024'
    """
    return ticket[YR:YR + 4] 

def get_month(ticket: str) -> str: 
    """Return the month of ticket 'ticket' in MM.
    
    >>> get_month('20230915YYZYEG12F')
    '09'
    >>> get_month('20241215YYZYEG12F1236')
    '12'
    """    
    return ticket[MON:MON + 2]
    
def get_day(ticket: str) -> str:
    """Return the day of the ticket 'ticket' in DD. 
    
    >>> get_day('20230915YYZYEG12F')
    '15'
    >>> get_day('20241211YYZYEG12F1236')
    '11'
    """
    return ticket[DAY:DAY + 2]

def get_departure(ticket: str) -> str:
    """Returns the departure of the ticket 'ticket' through airport code.
    
    >>> get_departure('20241215YYZYEG12F1236')
    'YYZ'
    >>> get_departure('20230915ORDYEG12F')
    'ORD'
    """
    
    return ticket[DEP:DEP + 3]

def get_arrival(ticket: str) -> str:
    """Returns the arrival of the ticket 'ticket' in airport code.
    
    >>> get_arrival('20230915YYZYEG12F12364')
    'YEG'
    >>> get_arrival('20230915YYZLAX12F12364')
    'LAX'
    """
    return ticket[ARR:ARR + 3]

def get_row(ticket: str) -> str:
    """Returns the row of the ticket 'ticket'.
    
    >>> get_row('20230915YYZLAX12F12364')
    '12'
    >>> get_row('20230915YYZLAX29F12364')
    '29'
    """
    return ticket[ROW:ROW + 2]

def get_seat(ticket: str) -> str:
    """Returns the seat number of the ticket 'ticket'.
    
    >>> get_seat('20230915YYZLAX29F12364')
    'F'
    >>> get_seat('20230915YYZLAX29R12364')
    'R'
    """
    return ticket[SEAT] 

def get_ffn(ticket:str) -> str:
    """Returns the four-digit frequent flyer number of the ticket 'ticket'.
    
    >>> get_ffn('20230915YYZYEG12F1236')
    '1236'
    >>> get_ffn('20230915YYZYEG12F')
    ''
    """
    return ticket[FFN:FFN + 4]

def is_valid_seat(ticket: str, first_row: int,last_row: int) -> bool:
    """Return True if and only if this ticket has a valid seat. That is,
    if the seat row is between 'first_row' and 'last_row', inclusive,
    and the seat is SA, SB, SC, SD, SE, or SF.

    Precondition: 'ticket' is in valid format.

    >>> is_valid_seat('20230915YYZYEG12F1236', 1, 30)
    True
    >>> is_valid_seat('20230915YYZYEG42F1236', 1, 30)
    False
    >>> is_valid_seat('20230915YYZYEG21Q1236', 1, 30)
    False
    """
    
    valid_row = first_row <= int(get_row(ticket)) <= last_row
    valid_seat = get_seat(ticket) in ('A','B','C','D','E','F')
    return valid_seat and valid_row

def is_valid_ffn(ticket: str) -> bool: 
    """Returns True if and only if the last four digits follow the conditions:
    The FFN numbers are the last four numbers of the ticket in which 
    the sum of the first three numbers modulo 10 is equal to the last digit. 
    A ticket will still valid if there are no FFN numbers, and will result 
    in True. 
    
    >>> is_valid_ffn('20230915YYZYEG21Q1236')
    True
    >>> is_valid_ffn('20230915YYZYEG21Q1337')
    True
    >>> is_valid_ffn('20230915YYZYEG21Q')
    True
    
    """
    if get_ffn(ticket) == '':
        return True
    
    digits = (int(ticket[FFN]) + int(ticket[FFN + 1]) + int(ticket[FFN + 2]))
    return digits % 10 == int(ticket[FFN + 3])

def is_valid_date(ticket: str) -> bool:
    """Returns True if the date of the ticket 'ticket is valid.
    The function also considers the days possible within each month,
    as well as for leap years in years of multiples of four. Exceptions include
    years of multiple 100 and includes years of multiple 400.
    
    >>> is_valid_date('20230915YYZYEG21Q1337')
    True
    >>> is_valid_date('20180229YYZYEG21Q')
    False
    >>> is_valid_date('20120229YYZYEG21Q')
    True
    >>> is_valid_date('16000229YYZYEG21Q')
    True
    >>> is_valid_date('14000229YYZYEG21Q1236')
    False
    """
    day = int(get_day(ticket))
    month = int(get_month(ticket))
    year = int(get_year(ticket))

    if len(get_year(ticket)) != 4 or len(get_month(ticket)) != 2:
            return False
        
    elif month < 1 or month > 12 or not (1 <= day <= 31):
            return False
        
    elif month in [4, 6, 9, 11] and day > 30:
            return False
        
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            if day > 29:
                return False
        elif day > 28:
            return False
    
    return True

def visits_airport(ticket: str, airport: str) -> bool:
    """Return True if and only if either departure or arrival airport on
    ticket 'ticket' is the same as 'airport'.
    
    >>> visits_airport('20230915YYZYEG12F1236', 'YEG')
    True
    >>> visits_airport('20230915YEGYYZ12F1236', 'YEG')
    True
    >>> visits_airport('20230915YYZYEG12F1236', 'YVR')
    False
    """    
    departure = get_departure(ticket)
    arrival = get_arrival(ticket)
    
    return arrival == airport or departure == airport

def connecting(ticket1: str, ticket2: str) -> bool:
    """Returns if two tickets 'ticket1' and 'ticket2' have connecting flights.
    The airport of ticket1 'ticket1' matches with the departure of ticket2
    'ticket2' on the same date.
    
    >>> connecting('20230915YYZYEG12C1236','20230915YEGYYZ12C1236')
    True
    >>> connecting('20230915YYZYEG12C1236','20230915YYZYEG12C1236')
    False
    """
    
    same_airport = get_arrival(ticket1) == get_departure(ticket2)
    same_date = get_date(ticket1) == get_date(ticket2)
    return (same_airport == same_date)

def get_seat_type(ticket: str) -> str:
    """Return 'window','aisle', or 'middle' depending on the type of seat in
    ticket 'ticket'. Exception also includes if there is no such seat type
    which it will return 'Invalid Seat Type'.

    Precondition: 'ticket' is a valid ticket.

    >>> get_seat_type('20230915YYZYEG12F1236')
    'window'
    >>> get_seat_type('20230915YYZYEG08B')
    'middle'
    >>> get_seat_type('20230915YYZYEG12C1236')
    'aisle'
    >>> get_seat_type('20230915YYZYEG1241236')
    'Invalid Seat Type'
    """
    if get_seat(ticket) == 'A' or get_seat(ticket) == 'F':
        return 'window'
    
    elif get_seat(ticket) == 'B' or get_seat(ticket) == 'E':
        return 'middle'
    elif get_seat(ticket) == 'D' or get_seat(ticket) == 'C':
        return 'aisle'
    else: 
        return 'Invalid Seat Type'

def adjacent(ticket1: str, ticket2: str) -> bool:
    """Returns 'Adjacent' if the tickets, 'ticket1' and 'ticket2 are
    matched together with seats. The seats 'A','B', 'C' are grouped together
    and the seats 'D', 'E', 'F'. They must be in the same rows. 
    The function also considers in case both tickets give the same seat, 
    which it will return 'Invalid due to same seat types'.
    
    >>> adjacent('20230915YYZYEG12C1236','20230915YYZYEG12A')
    True
    >>> adjacent('20230915YYZYEG12E1236','20230915YYZYEG12A')
    False
    >>> adjacent('20230915YYZYEG12A1236','20230915YYZYEG12A')
    'Invalid due to same seat types'
    >>> adjacent('20230915YYZYEG11C1236','20230915YYZYEG12A')
    False
    """
    
    ticket1_seat, ticket2_seat = get_seat(ticket1), get_seat(ticket2)
    adjacent_row1 = 'A','B','C'
    adjacent_row2 = 'D','E','F'
    
    if not (get_row(ticket1) == get_row(ticket2)):
        return False
    
    if ticket1_seat == ticket2_seat:
        return 'Invalid due to same seat types'
    elif ticket1_seat in adjacent_row1 and ticket2_seat in adjacent_row1:
        return True
    elif ticket1_seat in adjacent_row2 and ticket2_seat in adjacent_row2:
        return True
    else:
        return False
    
def behind(ticket1: str, ticket2:str) -> bool:
    """Returns True if the row of ticket2 'ticket2' is one behind ticket1
    'ticket1'.
    
    >>> behind('20230915YYZYEG12A1236','20230915YYZYEG12A')
    False
    >>> behind('20230915YYZYEG12A1236','20230915YYZYEG11A')
    True
    >>> behind('20230915YYZYEG99A9936','20230915YYZYEG98A')
    True
    """
    
    if get_seat(ticket1) == get_seat(ticket2):
        return int(get_row(ticket1)) == int(get_row(ticket2)) + 1
    else: return False

def is_valid_ticket_format(ticket: str) -> bool:
    """Return True if and only if ticket 'ticket' is in valid format:

    - year is 4 digits
    - months is 2 digits
    - day is 2 digits
    - departure is 3 letters
    - arrival is 3 letters
    - row is 2 digits
    - seat is a characters
    - frequent flyer number is either empty or 4 digits, and
      it is the last record in 'ticket'

    >>> is_valid_ticket_format('20241020YYZYEG12C1236')
    True
    >>> is_valid_ticket_format('20241020YYZYEG12C12361236')
    False
    >>> is_valid_ticket_format('ABC41020YYZYEG12C1236')
    False
    """
     
    return (FFN == 17
            and (len(ticket) == 17
                 or len(ticket) == 21 and ticket[FFN:FFN + 4].isdigit())
            and ticket[YR:YR + 4].isdigit()
            and ticket[MON:MON + 2].isdigit()
            and ticket[DAY:DAY + 2].isdigit()
            and ticket[DEP:DEP + 3].isalpha()
            and ticket[ARR:ARR + 3].isalpha()
            and ticket[ROW:ROW + 2].isdigit()
            and len(ticket[SEAT]) == 1)

def change_seat(ticket: str, row_number: str, seat: str) -> str:
    """Returns the ticket 'ticket' except with changed values from
    the row number 'row_number' and seat character 'seat'.
    
    >>> change_seat('20230915YYZYEG99A9936', '1', 'A')
    '20230915YYZYEG1A9936'
    >>> change_seat('20230915YYZYEG99A', '5', 'F')
    '20230915YYZYEG5F'
    """
    return ticket[YR: ROW] + row_number + seat + ticket[FFN:FFN +4]
   
def change_date(ticket: str, year:str, month:str, day:str) -> str:
    """Returns the ticket 'ticket' except with changed values from 
    year 'year', month 'month', and day 'day'.
    
    >>> change_date('20230915YYZYEG99A9936','2045','05','15')
    '20450515YYZYEG99A9936'
    >>> change_date('20230915YYZYEG99A','2024','12','15')
    '20241215YYZYEG99A'
    """
    return year + month + day + ticket[DEP:]
