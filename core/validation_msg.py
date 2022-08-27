from django.conf import settings

# General
WrongPhoneNumber   = "فرمت شماره تلفن وارد شده صحیح نمیباشد"
SomethingWentWrong = "مشکلی پیش آمده است"

# Login
LoginFieldEmpty     = "فیلد تلفن همراه نمیتواند خالی باشد"
LoginPhoneNotExists = "کاربری با این شماره تلفن یافت نشد"
LoginSmsSent        = "پیامک حاوی کد ورود برای شما ارسال شد"
LoginIncorrectCode  = 'کد وارد شده اشتباه است'
LoginTokenExpired   = 'توکن منقضی شده است'
LoginSuccesful      = 'خوش آمدید'
LoginIncorrect      = 'نام کاربری یا کلمه عبور اشتباه است'

# Reserve
ReserveTimeInvalid      = 'زمان انتخاب شده نامعتبر است'
ReserveNoDateSelected   = 'تاریخ و ساعت جلسه را مشخص کنید'
ReserveConflict         = 'زمان انتخاب شده با رزرو های دیگر تداخل دارد'
ReserveInPastNotAllowed = 'تاریخ و ساعت جلسه نمیتواند در گذشته رزرو شود!'
ReserveTimeLimited      = 'مدت زمان جلسه نمیتواند بیشتر از {} ساعت باشد'.format(settings.MAX_SESSION_TIME)
ReserveDayRangeLimit    = 'حداکثر زمان رزرو از امروز تا {} روز بعد امکان پذیر است'.format(settings.MAX_DAY_RANGE_TO_RESERVE)
ReserveCountPerDayLimit = 'حداکثر تعداد رزرو در یک روز {} عدد است'.format(settings.USER_MAX_SESSION_PER_DAY)
ReserveMinSecInvalid    = 'ساعت جلسه باید رند و کامل باشد'
ReserveTimeRangeInvalid = 'ساعات مجاز برای رزرو از {} تا {} است'.format(settings.SESSION_START_TIME, settings.SESSION_END_TIME)
ReserveNotFound         = 'رزرو یافت نشد'
ReserveIsDone           = 'جلسات به پایان رسیده امکان حذف ندارند'

# Admin
PhonenumberConflict = 'شماره موبایل وارد شده قبلا ثبت شده است'