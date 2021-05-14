from django import template
import datetime
register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "₹ "+str(number)

@register.filter(name='check_date')
def check_date(object):
    date = datetime.date.today()
    time = datetime.datetime.now().time()
    print(time)
    if date<object.date and time<object.start_time:
        return True
    else:
        return False


