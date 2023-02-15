from django.core.paginator import Paginator

#FUNCION QUE RETORNA UN DICCIONARIO CON LOS DATOS PAGINADOS, EL TOTAL DE PAGINAS Y LA PAGINA ACTUAL
def getElementosPaginados(paginaActual, model, serializador):
    data, paginador = {}, None
    if model.__name__ == 'Usuario':
        paginador = Paginator(model.objects.filter(is_active=True), 25)
    else:
        paginador = Paginator(model.objects.all(), 25)
    pagina = paginador.page(paginaActual)
    serializer = serializador(pagina.object_list, many=True)
    data['items'] = serializer.data
    data['totalPaginas'] = paginador.num_pages
    data['paginaActual'] = paginaActual
    return data