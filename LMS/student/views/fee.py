import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from admins.models.students import Students
from admins.models.fees import Fees, Student_fees, Academic_Year, Fee_discount
from .index import validate_user, get_notifications
import json
import razorpay
from django.conf import settings
keyid = settings.RAZORPAY_KEYID
keysecret = settings.RAZORPAY_KEYSECRET
razorpay_client = razorpay.Client(auth=(keyid, keysecret))


class View_Fee(View):
    def get(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Students, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification

            submit_fee = 0
            academic = Academic_Year.objects.all().order_by('academic_year').reverse()[0]
            user = get_object_or_404(Students, username=request.session.get('user'))

            data = {'user': user, 'notify': notify, 'notification': notification}
            try:
                class_fee = Fees.objects.get(class_name=user.class_name)
                total_fee = amount_after_discount(user,class_fee)
                if total_fee >0:
                    data['cls_fee'] = True

            except:
                total_fee = 0

            data['fee'] = total_fee

            student_fee = Student_fees.objects.filter(student=user,academic_year=academic)

            if len(student_fee)>0:
                for fee in student_fee:
                    submit_fee+=fee.amount

            data['student_fee']=student_fee
            data['submit_fee']= submit_fee
            if total_fee != 0:
                data['pending_fee'] = total_fee - submit_fee
            else:
                data['pending_fee'] = 0

            return render(request, 'students/fee-info.html', data)
        return redirect('login')

class PayFee(View):
    def get(self, request):
        if validate_user(request):
            ## for notification
            user = get_object_or_404(Students, username=request.session.get('user'))
            noti_info = get_notifications(user)
            notify = noti_info[0]
            notification = noti_info[1]
            # ------end  notification
            class_fee = Fees.objects.get(class_name=user.class_name)
            total_fee = amount_after_discount(user, class_fee)
            monthly = round(total_fee//12)
            data = {'user': user, 'fee':total_fee, 'monthly':monthly, 'notify':notify,'notification':notification }

            return render(request, 'students/pay_fee.html', data)
        return redirect('login')

    def post(self, request):
        if validate_user(request):
            user = get_object_or_404(Students, username=request.session.get('user'))
            class_fee = Fees.objects.get(class_name=user.class_name)
            total_fee = amount_after_discount(user, class_fee)
            academic = Academic_Year.objects.all().order_by('academic_year').reverse()[0]
            month = request.POST.get('month')
            amount = int(request.POST.get('amount'))
            payment = razorpay_client.order.create({'amount':amount*100, "currency":"INR", "payment_capture":"1"})
            callback_url = request.build_absolute_uri()+"payment_status/"
            try:
                student_fee = Student_fees.objects.get(student = user,academic_year=academic,amount = amount,month = month,status=False)
                student_fee.order_id = payment.get('id')
                student_fee.submit_date = datetime.datetime.now()

            except:
                student_fee = Student_fees(
                        student = user,
                        total_fee = total_fee,
                        academic_year=academic,
                        amount = amount,
                        month = month,
                        payment_mode = 'Online',
                        order_id = payment.get('id'),
                        status=False,
                        submit_date = datetime.datetime.now()
                )
            student_fee.save()
            data = {"amount":amount,"orderid":payment.get('id'),"callback_url":callback_url, "keyid":keyid}
            response = json.dumps(data, default=str)
            return HttpResponse(response)
        return redirect('login')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        data = request.POST
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')
        params_dict = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
        }
        try:
            student_fee = Student_fees.objects.get(order_id=order_id)
        except:
            return HttpResponse("Student_fee Not found")
        student_fee.payment_id = payment_id
        student_fee.order_id = order_id
        student_fee.save()
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        if result is None:
            student_fee.status = True
            student_fee.save()
            return render(request, 'payment/payment_success.html')
        else:
            return render(request, 'payment/payment_fail.html')

class Get_invoice(View):
    def get(self, request):
        if validate_user(request):
            submit_fee = 0
            user = get_object_or_404(Students, username=request.session.get('user'))
            total_fee = amount_after_discount(user,get_object_or_404(Fees, class_name=user.class_name))
            academic = Academic_Year.objects.all().order_by('academic_year').reverse()[0]
            data = {'user': user, 'fee':total_fee}
            student_fee = Student_fees.objects.filter(student=user,academic_year=academic, status=True)
            if len(student_fee)>0:
                for fee in student_fee:
                    submit_fee+=fee.amount
            data['student_fee']=student_fee
            data['pending_fee']=total_fee-submit_fee
            data['submit_fee']= submit_fee
            data['logo_path']= settings.BASE_DIR+"\static\img\logo\logo.png"

            pdf = render_to_pdf('payment/invoice.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
            # return render(request, 'payment/invoice.html', data)
        return redirect('login')


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)  # , link_callback=fetch_resources
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def amount_after_discount(student, class_fee):
    try:
        discount = Fee_discount.objects.get(student=student)
        total = class_fee.fees-(class_fee.fees*discount.discount)//100
    except:
        total = class_fee.fees
    return total

