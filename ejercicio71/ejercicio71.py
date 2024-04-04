import pandas as pd
import matplotlib.pyplot as plt

tabla = pd.read_csv('https://gitfront.io/r/DiegoPrueba1/PZnm9eE9nCdq/python-files/raw/madrid-airbnb-listings-apartado1.csv', sep=';', decimal='.')

tabla['precio'] = tabla['precio'].str.replace('$','')
tabla['precio'] = tabla['precio'].str.replace(',','')
tabla['precio'] = tabla['precio'].astype(float)

tabla.reset_index(inplace=True)

# Extraer la información requerida y crear una lista de diccionarios
lista_alojamientos = []
for index, row in tabla.iterrows():
    alojamiento = { 'id_alojamiento': row['index'],
        'id_anfitrion': row['anfitrion'],
        'distrito': row['distrito'],
        'precio': row['precio'],
        'plazas': row['plazas']}
    lista_alojamientos.append(alojamiento)


def num_alojamientos(lista):

    alojamientos_por_distrito = {}

    for alojamiento in lista:

        distrito = alojamiento['distrito']

        if distrito in alojamientos_por_distrito:

            alojamientos_por_distrito[distrito] +=1

        else:

            alojamientos_por_distrito[distrito] = 1

    
    plt.bar(alojamientos_por_distrito.keys(),alojamientos_por_distrito.values(), color='skyblue')
    plt.xlabel('Distritos')
    plt.ylabel('Número de alojamientos')
    plt.title('Número de Alojamientos por Distrito')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('c:/nueva/ejercicio71/diagrama_nalojamientos.png')
    plt.show()

recuento = num_alojamientos(lista_alojamientos)

#alojamientos = pd.DataFrame({'alojamientos': recuento})

#alojamientos.to_csv('c:/nueva/ejercicio67/alojamientos.csv', sep=';', decimal=',', index=True)

ocupantes = int(input("Indique el numero minimo de ocupantes que busca en el alojamiento: "))

def ocupantes_alojamientos(lista,ocupantes):

    ocupantes_por_alojamiento = []

    for plazas in lista:

        if plazas.get("plazas", 0) >= ocupantes:

            ocupantes_por_alojamiento.append(plazas)

    return ocupantes_por_alojamiento
    
resultado = ocupantes_alojamientos(lista_alojamientos, ocupantes)

ocupantesdf = pd.DataFrame(resultado)
ocupantesdf.to_csv('c:/nueva/ejercicio67/ocupantes.csv', sep=';', decimal=',', index=True)

listadistrito = tabla['distrito'].unique().tolist()

testigo = False

while testigo == False:

    distrito = input("Introduce el distrito donde quieres buscar el alojamiento: ").capitalize()

    if distrito in listadistrito:

        testigo = True
        print('El distrito esta en la lista')

    else:

        testigo = False
        print('El distrito no está en la lista')

def alojamientos_baratos(lista, distrito):

    alojamientos_distrito = [alojamiento for alojamiento in lista if alojamiento.get("distrito") == distrito]
    alojamientos_distrito.sort(key=lambda x: x.get("precio"))
    return alojamientos_distrito[:10]

resultado1 = alojamientos_baratos(lista_alojamientos, distrito)

baratos = pd.DataFrame(resultado1)

baratos.to_csv('c:/nueva/ejercicio67/baratos.csv', sep=';', decimal=',', index=True)

def anfitriones(lista):

    alojamientos_por_anfitrion = {}

    for alojamiento in lista:

        anfitrion = alojamiento['id_anfitrion']

        if anfitrion in alojamientos_por_anfitrion:

            alojamientos_por_anfitrion[anfitrion] +=1

        else:

            alojamientos_por_anfitrion[anfitrion] = 1

    return alojamientos_por_anfitrion

resultado2 = anfitriones(lista_alojamientos)


listaalojamientos = pd.DataFrame({'alojamientos':resultado2})

listaalojamientos.to_csv('c:/nueva/ejercicio67/listaalojamientos.csv', sep=';', decimal=',', index=True)


tabla2 = pd.read_csv('https://gitfront.io/r/DiegoPrueba1/PZnm9eE9nCdq/python-files/raw/madrid-airbnb-listings-apartado6.csv', sep=';', decimal=',')

tabla2['precio_persona'] = tabla2['precio_persona'].round(2).convert_dtypes()

tabla2['distrito'] = tabla2['distrito'].astype(str)
distrito = tabla2['distrito'].unique().tolist()
tabla2['tipo_alojamiento'] = tabla2['tipo_alojamiento'].astype(str)
tipoalojamiento_lista = tabla2['tipo_alojamiento'].unique().tolist()


while testigo == False:

    distrito1 = input("Introduce el distrito para dibujar el diagrama de sectores: ").capitalize()

    if distrito1 in distrito:

        testigo = True
        print('El distrito esta en la lista')

    else:

        testigo = False
        print('El distrito no está en la lista')


def por_aloj_distrito (distritos):

    filtrado_distritos = tabla2[tabla2['distrito'].isin(distritos)]

    tipos_alojamientos = filtrado_distritos.groupby(['distrito','tipo_alojamiento']).size().groupby(level=0).cumsum().groupby(level=0).transform(lambda x: x / x.iloc[-1] * 100).round(2).convert_dtypes()
    #tipos_alojamientos = filtrado_distritos.groupby('distrito')['tipo_alojamiento'].value_counts().unstack().fillna(0) 
    #porcentaje = (tipos_alojamientos.div(tipos_alojamientos.sum(axis=1), axis=0)*100).round(2) #Porcentaje por tipos de alojamientos
    #porcentaje = porcentaje.sort_values(by='tipo_alojamiento',ascending=False)
    #alojamientos_pordistrito = porcentaje.to_dict (orient='index')

    #return tipos_alojamientos
    fig, ax = plt.subplots()
    tipos_alojamientos.unstack().plot(kind='bar', stacked=False, ax=ax)
    ax.set_xlabel('Distritos')
    ax.set_ylabel('Porcentaje  acumulados de alojamientos')
    ax.set_title('Porcentaje de tipos de alojamientos por distrito ')
    ax.legend(title='Tipo de alojamiento')
    plt.tight_layout()
    plt.savefig('c:/nueva/ejercicio71/diagrama_porcentaje.png')
    plt.show()

resultado3 = por_aloj_distrito(distrito)
#print(resultado3)

#poralojdistritos = pd.DataFrame(resultado3)

#poralojdistritos.to_csv('c:/nueva/ejercicio67/poralojamientos.csv', sep=';', decimal=',', index=True)

def alojamientosanfitrion(distritos):

    filtrado_distritos = tabla2[tabla2['distrito'].isin(distritos)]

    alojamientos_poranfitrion = filtrado_distritos.groupby(['anfitrion','distrito']).size().unstack(fill_value=0)
    alojamientos_poranfitrion['total'] = alojamientos_poranfitrion.sum(axis=1)
    alojamientos_poranfitrion = alojamientos_poranfitrion.sort_values(by='total', ascending=False)
    alojamientos_poranfitrion = alojamientos_poranfitrion.drop(columns=['total'])
    alojamientosdict = alojamientos_poranfitrion.to_dict(orient='index')

    return alojamientosdict

resultado4 = alojamientosanfitrion(distrito)

alojanfitriones = pd.DataFrame(resultado4)

alojanfitriones.to_csv('c:/nueva/ejercicio67/totalanfitriones.csv', sep=';', decimal=',', index=True)

def mediaalojaporanfi(distritos):

    filtrado_distritos = tabla2[tabla2['distrito'].isin(distritos)]
    alojamientos_medioanfitrion = filtrado_distritos.groupby(['anfitrion','distrito']).size().unstack(fill_value=0)
    alojamientos_medioanfitrion['total'] = alojamientos_medioanfitrion.mean(axis=0)
    alojamientosmediodict = alojamientos_medioanfitrion.to_dict(orient='index')

    return alojamientosmediodict

resultado5 = mediaalojaporanfi(distrito)

mediatabla = pd.DataFrame(resultado5)

mediatabla.to_csv('c:/nueva/ejercicio67/media.csv', sep=';', decimal=',', index=True)

def distrito_tipoaloja(distrito,tipo):

    filtrado = tabla2[(tabla2['distrito'].isin(distrito)) & (tabla2['tipo_alojamiento'].isin(tipo))]

    dffiltrado = filtrado[['distrito','anfitrion','tipo_alojamiento']]

    df_distribucion = dffiltrado.groupby(['distrito', 'anfitrion', 'tipo_alojamiento']).size().unstack(fill_value=0)

    df_distribucion['Total'] = df_distribucion.sum(axis=1)

    distrito_seleccionado = distrito[1]

    distrito_seleccionado = df_distribucion.loc[distrito_seleccionado]

    if not distrito_seleccionado.empty:

        sin_total = distrito_seleccionado.drop('Total', axis=1)
        datos_diagrama = sin_total.sum()

        plt.pie(datos_diagrama, autopct='%1.1f%%')
        plt.title(f'Distribución de alojamientos por anfitrión en {distrito_seleccionado}')
        plt.tight_layout()
        plt.savefig('c:/nueva/ejercicio71/diagrama_desectores.png')
        plt.show()

    else:
       
        print(f"No hay datos disponibles para el distrito {distrito_seleccionado}.")
    
resultado6 = distrito_tipoaloja(distrito,tipoalojamiento_lista)

def dia_por_persona(dataframe):

    #mediaporpersona = dataframe['precio_persona'].mean()
    #dia_decadadistrito = dataframe.groupby('distrito')['precio_persona'].mean().round(2)
    preciomedio = dataframe.groupby('distrito')['precio_persona'].mean().round(2)
    diamedio = dataframe.groupby('distrito')['noches_minimas'].mean().round(2)
    mediaprecio_dia = preciomedio/diamedio
    fig, ax = plt.subplots()
    mediaprecio_dia.plot(kind='bar', color='skyblue')
    ax.set_xlabel('Distritos')
    ax.set_ylabel('Precio medio por persona y dia')
    ax.set_title('Precio medio por persona y dia por distrito ')
    plt.tight_layout()
    plt.savefig('c:/nueva/ejercicio71/diagrama_preciosmedios.png')
    plt.show()

resultado7 = dia_por_persona(tabla2)

def costeminimovspuntuacion(distrito):

    filtrado = tabla2[tabla2['distrito'].isin(distrito)]

    minporpersona = filtrado.groupby('distrito')['precio_persona'].min()
    pun_distrito = filtrado.groupby('distrito')['puntuacion'].mean()

    plt.scatter(minporpersona,pun_distrito, color='blue')
    plt.title('Costo mínimo por noche y persona vs. Puntuación por distrito')
    plt.xlabel('Costo mínimo por noche y persona')
    plt.ylabel('Puntuación promedio')
    plt.tight_layout()
    plt.savefig('c:/nueva/ejercicio71/diagrama_dispersion.png')
    plt.show()

resultado8 = costeminimovspuntuacion(distrito)

def distribucion_precios(distritos):

    filtrado = tabla2[tabla2['distrito'].isin(distritos)]
    filtrado.groupby('distrito')['precio_persona'].mean().plot(kind='bar', color='skyblue')
    plt.xlabel('Distrito')
    plt.ylabel('Precio promedio por persona y día')
    plt.title('Distribución de precios por persona y día en cada distrito')
    plt.tight_layout()
    plt.savefig('c:/nueva/ejercicio71/diagrama_distribucion.png')
    plt.show()

resultado9 = distribucion_precios(distrito)



    
















