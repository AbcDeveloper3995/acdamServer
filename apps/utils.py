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

# Funcion que retorna el nombre de la provincia en su formato largo
def formatoLargoProvincia(slug):
        if slug == 'PR':
            return 'Pinar del Rio'
        elif slug == 'ART':
            return 'Artemisa'
        elif slug == 'MAY':
            return 'Mayabeque'
        elif slug == 'HAB':
            return 'La Habana'
        elif slug == 'MAT':
            return 'Matanzas'
        elif slug == 'VCL':
            return 'Villa Clara'
        elif slug == 'CFG':
            return 'Cienfuegos'
        elif slug == 'SS':
            return 'Santi Spiritu'
        elif slug == 'CAV':
            return 'Ciego de Avila'
        elif slug == 'TUN':
            return 'Las Tunas'
        elif slug == 'HOL':
            return 'Holguin'
        elif slug == 'GRM':
            return 'Granma'
        elif slug == 'STG':
            return 'Santiago de Cuba'
        elif slug == 'GTM':
            return 'Guantanamo'
        elif slug == 'IJV':
            return 'Isla de la Juventud'