from django.db.models import (
    Model,
    TextField,
    ForeignKey,
    RESTRICT,
    ManyToManyField,
    IntegerChoices,
    BigIntegerField,
    IntegerField,
)

from auther.models import User
from fancy.models import SafeDeleteModel, LogFieldsModel


class Product(SafeDeleteModel, LogFieldsModel):
    name = TextField(null=True)


class Price(SafeDeleteModel, LogFieldsModel):
    product = ForeignKey(Product, on_delete=RESTRICT, related_name='prices', null=True)
    amount = BigIntegerField(null=False)


class Package(Product):
    products = ManyToManyField(Product, related_name='packages')


class Subscribe(Product):
    duration = IntegerField(null=True)


class Order(SafeDeleteModel, LogFieldsModel):
    user = ForeignKey(User, on_delete=RESTRICT, related_name='orders')
    products = ManyToManyField(Product, related_name='orders', through='Item')


class Item(Model):
    order = ForeignKey(Order, on_delete=RESTRICT, related_name='items')
    product = ForeignKey(Product, on_delete=RESTRICT, related_name='items')
    price = ForeignKey(Price, on_delete=RESTRICT, related_name='items', null=True)


class Payment(SafeDeleteModel, LogFieldsModel):
    class Type(IntegerChoices):
        REMISSION = 1
        CASH = 2
        ONLINE = 3
        FREE = 4

    order = ForeignKey(Order, on_delete=RESTRICT, related_name='payments', null=True)
    type_id = IntegerField(null=True, choices=Type.choices)
    identity_token = TextField(null=True)
    ref_id = TextField(null=True)
