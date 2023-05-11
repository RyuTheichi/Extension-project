from django.shortcuts import render
from django.views import View
from cliente.models import MenuItem, OrderModel , Categoria



class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cliente/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cliente/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # pegar cada item de uma categoria
        hamburgers = MenuItem.objects.filter(categoria__nome__contains='hamburgers')
        acompanhamentos = MenuItem.objects.filter(categoria__nome__contains='Acompanhamentos')
        adicionais = MenuItem.objects.filter(categoria__nome__contains='Adicionais')
        bebidas = MenuItem.objects.filter(categoria__nome__contains='Bebidas')

        # contextualizar
        context = {
            'hamburgers': hamburgers,
            'acompanhamentos': acompanhamentos,
            'adicionais': adicionais,
            'bebidas': bebidas,
        }

        # rendererizar o template
        return render(request, 'cliente/order.html', context)

    def post(self, request, *args, **kwargs):
        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'nome': menu_item.nome,
                'preco': menu_item.preco,
            }

            order_items['items'].append(item_data)

            preco = 0
            item_ids = []

        for item in order_items['items']:
            preco += item['preco']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(preco=preco)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'preco': preco
        }

        return render(request, 'cliente/order_confirmation.html', context)