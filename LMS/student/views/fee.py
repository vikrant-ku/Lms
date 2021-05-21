from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from admins.models.students import Students
from admins.models.fees import Fees, Student_fees, Academic_Year
from .index import validate_user
import json
import razorpay
from django.conf import settings
keyid = settings.RAZORPAY_KEYID
keysecret = settings.RAZORPAY_KEYSECRET
razorpay_client = razorpay.Client(auth=(keyid, keysecret))



class View_Fee(View):
    def get(self, request):
        if validate_user(request):
            submit_fee = 0
            academic = Academic_Year.objects.all().order_by('academic_year').reverse()[0]
            user = get_object_or_404(Students, username=request.session.get('user'))
            class_fee = get_object_or_404(Fees, class_name=user.class_name)
            data = {'user': user, 'fee':class_fee}
            student_fee = Student_fees.objects.filter(student=user,academic_year=academic)

            if len(student_fee)>0:
                for fee in student_fee:
                    submit_fee+=fee.amount

            data['student_fee']=student_fee
            data['pending_fee']=class_fee.fees-submit_fee
            data['submit_fee']= submit_fee

            return render(request, 'students/fee-info.html', data)
        return redirect('login')

class PayFee(View):
    def get(self, request):
        if validate_user(request):
            user = get_object_or_404(Students, username=request.session.get('user'))
            total_fee = get_object_or_404(Fees, class_name=user.class_name)
            monthly = round(total_fee.fees//12)
            data = {'user': user, 'fee':total_fee, 'monthly':monthly}

            return render(request, 'students/pay_fee.html', data)
        return redirect('login')

    def post(self, request):
        if validate_user(request):
            user = get_object_or_404(Students, username=request.session.get('user'))
            total_fee = get_object_or_404(Fees, class_name=user.class_name)
            academic = Academic_Year.objects.all().order_by('academic_year').reverse()[0]
            month = request.POST.get('month')
            amount = int(request.POST.get('amount'))
            print('month ',month)
            payment = razorpay_client.order.create({'amount':amount*100, "currency":"INR", "payment_capture":"1"})
            callback_url = request.build_absolute_uri()+"handle_request/"
            student_fee = Student_fees(
                    student = user,
                    total_fee = total_fee,
                    academic_year=academic,
                    amount = amount,
                    month = month,
                    payment_mode = 'Online',
                    order_id = payment.get('id'),
                    status=False
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
            class_fee = get_object_or_404(Fees, class_name=user.class_name)
            academic = Academic_Year.objects.all().order_by('academic_year').reverse()[0]
            data = {'user': user, 'fee':class_fee}
            student_fee = Student_fees.objects.filter(student=user,academic_year=academic, status=True)
            if len(student_fee)>0:
                for fee in student_fee:
                    submit_fee+=fee.amount
            data['student_fee']=student_fee
            data['pending_fee']=class_fee.fees-submit_fee
            data['submit_fee']= submit_fee
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
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)  # , link_callback=fetch_resources
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None








