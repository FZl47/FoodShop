from Food.models import Discount

def delete_discount(id):
    try:
        discount = Discount.objects.get(id=id)
        discount.delete()
    except:
        pass