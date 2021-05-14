from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from admins.models.students import Students
from admins.models.fees import Fees, Student_fees
from .index import validate_user


class View_Fee(View):
    def get(self, request):
        if validate_user(request):
            submit_fee = 0
            user = get_object_or_404(Students, username=request.session.get('user'))
            class_fee = get_object_or_404(Fees, class_name=user.class_name)
            data = {'user': user, 'fee':class_fee}
            student_fee = Student_fees.objects.filter(student=user)
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
            monthly = round(total_fee.fees/12,2)
            data = {'user': user, 'fee':total_fee, 'monthly':monthly}
            return render(request, 'students/pay_fee.html', data)
        return redirect('login')

    def post(self, request):
        if validate_user(request):
            user = get_object_or_404(Students, username=request.session.get('user'))
            total_fee = get_object_or_404(Fees, class_name=user.class_name)

            month = request.POST.get('month')
            amount = request.POST.get('amount')
            try:
                fee = get_object_or_404(Student_fees, student=user.id, month=month)
                if fee.status == True:
                    messages.error(request, f"You Submit your {fee.month} fee on {fee.submit_date.date()}.")
                    return redirect('view_fee')
            except:
                pass
            student_fee = Student_fees(
                student = user,
                total_fee = total_fee,
                amount = amount,
                month = month,
                payment_mode = 'Online',
                txn_no = "tyx-jsdud5dkd745d",
                status=True
            )
            student_fee.save()
            messages.success(request, f" your {student_fee.month} fee has been Submitted. ")
            return redirect('view_fee')
        return redirect('login')


