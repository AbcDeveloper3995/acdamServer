import datetime

from django.core.paginator import Paginator

from apps.recaudacion.models import Recaudacion

#FUNCION QUE RETORNA UN DICCIONARIO CON LOS DATOS PAGINADOS, EL TOTAL DE PAGINAS Y LA PAGINA ACTUAL
def getElementosPaginados(paginaActual, model, serializador, id=None):
    data, paginador = {}, None
    if model.__name__ == 'Credito' and id == '': #Este caso es unicamente para la carga inicial no de error
        date = datetime.datetime.now().date()
        try:
            paginador = Paginator(model.objects.filter(fk_recaudacion__fechaCreacion=date), 25)
        except:
            paginador = Paginator(model.objects.none(), 1)
    elif model.__name__ == 'Credito' and id != '':
        obj = Recaudacion.objects.get(pk=id)
        paginador = Paginator(model.objects.filter(fk_recaudacion__fechaCreacion=obj.fechaCreacion), 25)
    elif model.__name__ == 'Usuario':
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

#FUNCION PARA OBTENER LA FECHA DE VENCIMIENTO DE UN CONTRATO
def getFechaExpiracion(anos):
    date = datetime.datetime.today().date()
    year = date.year + anos
    return datetime.datetime(year, date.month, date.day).date()

#FUNCION PARA OBTENER LA DESCRIPCION DE LA PERIOCIDAD DE ENTREGA
def getDescripcionPeriocidadEntrega(value):
    if value == '1':
        return 'Trimestral musica viva'
    else:
        return 'Bianual musica grabada'