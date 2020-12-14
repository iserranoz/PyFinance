import streamlit as st 
import pandas as pd 
import numpy as np
import pandas_datareader as web
import plotly_express as px
import plotly.graph_objs as go
import datetime
from iexfinance.stocks import Stock
from datetime import datetime
from iexfinance.stocks import get_historical_data
from iexfinance.iexdata import get_last
from datetime import datetime
from iexfinance.stocks import get_historical_intraday
import time
import requests
import os
import lxml.html as html
import datetime
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from newspaper import Article
from datetime import datetime
from fpdf import FPDF


def gt():
	#esta funcion no recibe inputs, lee el archivo txt para obtener el token del usuario 
    f = open ('token.txt','r')
    token = f.read()
    f.close()
    return token


def hora():
	#funcion que nos genera l ahora actual
	return str(datetime.datetime.now().time())

def close():
	#función que genera la linea de precio de cierre
	return fig1.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines',line=dict(color='red'), name = 'Close Price'))


def Open():
	#función que genera la linea de precio de de apertura
	return fig1.add_trace(go.Scatter(x=df.index, y=df['Open'], mode='lines',line=dict(color='green'), name = 'Open Price'))


def SMA():
	#función que genera la linea de simple moving average
	return fig1.add_trace(go.Scatter(x=df.index, y=df['SMA'], mode='lines',line=dict(color='blue'), name = 'Simple Moving Average'))


def EMA():
	#función que genera la linea de exponencial moving average
	return fig1.add_trace(go.Scatter(x=df.index, y=df['EMA'], mode='lines',line=dict(color='yellow'), name = 'Exponencial Moving Average'))


def upper():
	#función que genera la linea de las bolinger bandas
	return fig1.add_trace(go.Scatter(x=df.index, y=df['Upper'], mode='lines',line=dict(color='black', width = .7), name = 'Bolinger Upper'))


def lower():
	#función que genera la linea de las bolinger bandas
	return fig1.add_trace(go.Scatter(x=df.index, y=df['Lower'], mode='lines',line=dict(color='black', width = .7), name = 'Bolinger Lower'))

def p_ent(enter):
	#función que genera la linea del enter point
	return fig1.add_trace(go.Scatter(x = df.index, y = [enter for i in df.index], mode = 'lines', name = 'Enter point'))

def p_stop(stop):
	#función que genera la linea del stop loss
	return fig1.add_trace(go.Scatter(x = df.index, y = [stop for i in df.index], mode = 'lines', name = 'Stop Loss'))
	

def generate_stock(symbol,start, end):
	#función para generar el stock solicitado
    data = web.DataReader(symbol, data_source = 'yahoo', start = start,end = end)
    return data

def statistics(symbol):
	#función de obteneción de estadísticas    
    statistics = pd.read_html(f'https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}')
    valuation_measures = pd.DataFrame(statistics[0])
    valuation_measures.rename(columns={valuation_measures.columns[0]: 'Valuation Measures', valuation_measures.columns[1]: 'Current'}, inplace=True)
    valuation_measures['Valuation Measures'] = valuation_measures['Valuation Measures'].apply(lambda x:x[0:-1] if x[-1].isdigit() else x)
    balance_sheet = pd.DataFrame(statistics[8])
    balance_sheet.rename(columns={balance_sheet.columns[0]: 'Balance Most Recent Quarter', balance_sheet.columns[1]: 'Value'}, inplace=True)
    balance_sheet['Balance Most Recent Quarter'] = balance_sheet['Balance Most Recent Quarter'].apply(lambda x:x[0:-6])
    income_statement = pd.DataFrame(statistics[7])
    income_statement.rename(columns={income_statement.columns[0]: 'Income Statement', income_statement.columns[1]: 'Value'}, inplace=True)
    return valuation_measures,balance_sheet, income_statement

def profile(symbol):
	#función para obtención de información de la empresa
    profile = pd.read_html(f'https://finance.yahoo.com/quote/{symbol}/key-profile?p={symbol}')
    profile1 = pd.DataFrame(profile[0])
    profile2 = pd.DataFrame(profile[1])
    frames = [profile1, profile2]
    prof = pd.concat(frames)
    prof.rename(columns={prof.columns[0]: 'Indicator', prof.columns[1]: 'Value'}, inplace=True)
    ind = ['Previous Close','Open',"Day's Range",'Volume','Avg. Volume','Market Cap','Beta (5Y Monthly)','PE Ratio (TTM)','PE Ratio (TTM)','EPS (TTM)']
    prof = prof[prof['Indicator'].isin(ind)]
    return prof 

def getCompanyInfo(symbol):
	#función para obtención de información de la empresa
    stock_batch = Stock(symbol,
                        token=token)
    company_info = stock_batch.get_company()
    return company_info

def live(symbol):
    #función para obtener precios intraday
    df = get_historical_intraday(symbol, date.today(),token = token,output_format='pandas')
    
    return df

def candle_intra(df):
	#función de generación de gráfica de velas
    df['EMA'] = df['close'].ewm(span=21,adjust = False).mean()
    df['SMA'] = df['close'].rolling(window = 20).mean()
    fig2 = go.Figure(data = [go.Candlestick(x= df.index,
                                   close= df['close'],
                                 high = df['high'],
                                    low =df['low'],
                                    open = df['open'],                 
                                    increasing_line_color = 'green',
                                   decreasing_line_color = 'red', name = '')])
       
    fig2.add_trace(go.Scatter(x=df.index, y=df['SMA'], mode='lines',line=dict(color='blue',width = 1), name = 'SMA'))
    fig2.add_trace(go.Scatter(x=df.index, y=df['EMA'], mode='lines',line=dict(color='orange',width = 1), name = 'EMA'))
        
    fig2.update_layout(xaxis_rangeslider_visible=True, width =500)
    return fig2


def news(url):
	#función de scraping del washington post
    url_base = url
    response = requests.get(url_base)
    home = response.content.decode('utf-8')
    parsed = html.fromstring(home)
    links = '//div/h2/a/@href'
    links_2 = parsed.xpath(links)
    return links_2

def art(article):
	#función para obtención de titulo, fecha y cuerpo
	article = Article(article)
	article.download()
	article.parse()
	nltk.download('punkt')
	article.nlp()
	return article

def art_es(article):
	#función para obtención de titulo, fecha y cuerpo
	article = Article(article, language='es')
	article.download()
	article.parse()
	nltk.download('punkt')
	article.nlp()
	return article

def news_w():
	#función de scraping del new york times
    url_base = 'https://www.nytimes.com/world' 
    response = requests.get(url_base)
    home = response.content.decode('utf-8')
    parsed = html.fromstring(home)
    links = '//div/h2/a/@href'
    links_2 = parsed.xpath(links)
    links_2 = ['https://www.nytimes.com' +i for i in links_2 ]
    return links_2

def universal(url):
	##función de scraping del universal
    response = requests.get(url)
    home = response.content.decode('utf-8')
    parsed = html.fromstring(home)
    links = '//div/p/a/@href'
    links_2 = parsed.xpath(links)
    return links_2

def universal2(url):
	##función de scraping del universal
    response = requests.get(url)
    home = response.content.decode('utf-8')
    parsed = html.fromstring(home)
    links = '//div/h2/a/@href'
    links_2 = parsed.xpath(links)
    return links_2

def ganancia(uno, dos):
	try:
		g = ((uno-dos)/uno)
	except:
		g = 0
	return g*100 


class PDF(FPDF):
    #generación de pdf de noticias
    def logo(self, name,x,y,w,h):
        self.image(name,x,y,w,h)
    
    def texts(self,name):
        with open(name, 'rb') as xy:
            txt = xy.read().decode(encoding="latin-1")
        self.set_xy(10.0,80.0)
        self.set_text_color(0,0,0)
        self.set_font('Helvetica', '', 8)
        self.multi_cell(0,5,txt)
        
    def titles(self, title):
        self.set_xy(0.0,0.0)
        self.set_font('Times')
        self.set_text_color(0,0,0)
        self.cell(w = 210.0, h = 40.0, align = 'C', txt = title, border = 0)
      


	


st.set_page_config(page_title='Financial',page_icon = '📈')


nav = st.sidebar.selectbox("Menu",['Home',"Profile","Charts","Statistics",'Market Live', "News Paper", "Market Simulator"])

if nav == "Home":

	col1 , col2 = st.beta_columns([4,1])
	col2.subheader('')
	col2.subheader('')
	col2.subheader('')
	col2.subheader('')
	
	df = pd.read_csv('companies.csv', index_col = 'Unnamed: 0')
	col2.image('IRONHACK.png',width = 120, use_column_width = False)
	col2.subheader('')
	col2.image('st.png',width = 120, use_column_width = False)
	col2.subheader('')
	col2.image('py.png',width = 70, use_column_width = False)
	#col1.header('Py Finance')
	col1.image('logo.png',width = 180)
	col1.subheader('')

	col1.subheader('Presentación')
	col1.markdown('¿Qué es PyFinance?')
	col1.markdown('Py Finance es un aplicación desarrolada en Python y soportada por Streamlit, la cual nos permite convertir scripts de datos en aplicaciones Web')
	col1.subheader('')
	col1.markdown('¿Qué nos ofrece PyFinance?')
	col1.markdown('PyFinance nos ofrece información de empresas que cotizan en el mercado en tiempo real de una forma rapida y sencilla.')
	col1.markdown('Podemos consultar la información más relevante de la empresa y sus cotizaciones históricas, visualizar sus gráficos y generar indicadores, consultar estadísticas y leer noticias del momento')
	col1.markdown('Extraer, procesar, visualizar y analizar información financiera')
	col1.subheader('')
	col1.subheader('')
	col1.subheader('Estructura de la aplicación')
	with col1.beta_expander("Mostrar descripción"):
	    	st.write("""
        	La estructura de la aplicación se compone de las siguientes opciones:

        	1. Profile

        	   Podemos visualizar información relevante de la compañia, último precio de cotización, sitio web, dirección y  consultar sus datos históricos y descargarlos.

        	2. Charts

        	   Nos ofrece una visualización amigable de los precios, tanto de cierre, como de apertura, también, es posible
        	   cambiar el diseño de la gráfica de lineas por una de velas. Esta pestaña cuenta con la visualización de algunos indicadores como Volumen, RSI, MACD, Bandas de Bolinger,
        	   Simple Moving Average y Exponencial Moving Average.

        	3. Statistics

        	   Despliega las estádisticas más relevantes de la compañia como medidas de valoracion de los ultimos cuatro trimestres, Balance de la compañia y su Estado de resultados.

        	4. Market Live

        	   Visaulización de precios intradía de cualquier acción, junto con varias herramientas para el análisis técnico, esta grafica cuenta con un boton de actualización
        	   que nos actualiza los precios que se generan por intervalos de 1 minuto.

        	5. News Paper

        	   Esta sección se compone de los resumenes de noticias de diferentes fuentes como; Washington Post, New York Times y El Universal. Se puede buscar por sección
        	   y también puedes generar y descargar un PDF del texto de la noticia.

        	6. Market Simulator

        	   Esta pestaña nos permite simular la operación en vivo del mercado con precios intradía, podemos usar tres paneles de graficas con una panel de información,
        	   esta sección aún no está optimizada aunque presenta un primer avance de la idea.""")
        
	with col1.beta_expander("Mostrar fuentes de información"):
    		st.write("""

        	APis

        	https://finance.yahoo.com/quotes/API,Documentation/view/v1/

        	https://iexcloud.io/

        	Páginas web 
        	
        	https://www.washingtonpost.com/

        	https://www.nytimes.com/

        	https://www.eluniversal.com.mx/
        	.""")
        	


    
	with col1.beta_expander("Información del desarrollador"):
    		st.write("""

        	Github   | https://github.com/iserranoz

        	Linkedin | https://www.linkedin.com/in/ivan-serrano035/

        	Mail     | iserranoz35@gmail.com

        	Iván Alberto Serrano Zapata
        	""")



   
	if col1.checkbox('Compañías disponibles'):
		col1.write(df)
	
	col1.subheader('Consideraciones')
	col1.markdown('Si es primera vez que usas PyFinance, por favor sigue las siguientes instrucciones, si no, omítelos.')
	col1.markdown("""
			Para poder ejecutar todas las herramientas que nos proporciona PyFinance necesitamos establecer
			una conexión a la APi de IEX CLOUD, la cual nos otorga un Token personal. Sigue los siguientes pasos,
			el registro demora 2 minutos y el proceso de aprobación es instantaneo, solo necesitas un correo electrónico.

        	1. Entra al link de la parte inferior, 
        	teclea tu correo y dale Start Now.

        	2. Te enviarán instantaneamente un mail de verificación, 
        	da click y listo tendrás tu cuenta de IEX CLOUD.""")
	col1.markdown('https://iexcloud.io/')
	col1.markdown('3. Una vez que estamos registrados observaremos nuestra consola, da click en API Tokens')
	col1.image('IEX1.png',width = 120, use_column_width = True)
	col1.markdown('4. Da click en Reveal secret token, copia tu token personal y pegalo en la casilla de abajo, luego Submit y listo, podemos comenzar.')
	col1.image('IEX2.png',width = 120, use_column_width = True)
	token=col1.text_input('Enter Token')
	if col1.button('Guardar'):
		f=open('token.txt',"w",encoding="utf-8")
		f.write(token)
		f.close()
		col1.success('DONE')
	col1.markdown('Mensaje a la comunidad')
	col1.write("""
				Esta versión de PyFinance es la primera, el proyecto es completamente escalable, por lo que invito a cualquier interesado a contactarme, 
	        	cualquier tipo de aportación es completamente bienvenida, desde la propuesta para mejorar de las funcionalidades con las cuenta la aplicación, 
	        	hasta agregar nuevas herramientas o incluso secciones.
	        	Mis datos de contacto los pueden encontrar en la parte inferior, en la pestaña información del desarrollador.
	        	Si no sabes en que ayudar, la pestaña de Market Simulator presenta una buena aproximación a lo que sería la interacción en tiempo real con el trading,
	        	pero, aún no es lo suficientemente óptima en cuanto a velocidad y herramientas.""")
	if col1.button('Mensaje'):
		col1.success('"Si lo puedes imaginar, lo puedes programar"')





if nav == "Profile":
	st.header('Profile')
	col1 , col2 = st.beta_columns(2)
	symbol = col1.text_input ('Enter Symbol','AMZN')
	token = gt()

	col1 , col2 = st.beta_columns(2)
		
	profile = profile(symbol)
	info = getCompanyInfo(symbol)
	st.subheader(symbol)
	col1.subheader('Profile')
	col1.info(f" Last Price {get_last(symbols=symbol, token = token)[0]['price']}")
	col1.write(profile)
	col2.subheader('Company Info')
	col2.info(f"Name  | {info['companyName']}")
	col2.info(f"Exchange  | {info['exchange']}")
	col2.info(f"Website  | {info['website']}")
	col2.info(f"State  | {info['state']}")
	col2.info(f"Country  | {info['country']}")
	col1 , col2 = st.beta_columns(2)
	start = col1.date_input ('Start', datetime.strptime('2020-10-1', '%Y-%m-%d'))
	end = col2.date_input('End')
	if col1.button('Show historical data'):
		col1 , col2 = st.beta_columns(2)
		df = generate_stock(symbol,start, end)
		st.subheader('Historical data')
		st.write(df)
	if st.button("Download data"):
		
		df = generate_stock(symbol,start, end)
		st.write(df)
		df.to_csv(f'{symbol}.csv')
		st.success("Done")

		


if nav == "Charts":
	token = gt()
	st.header('Charts')
	col1 , col2, col3, col4 = st.beta_columns(4)
	symbol = col1.text_input ('Enter Symbol','AMZN')
	start = col2.date_input ('Start', datetime.strptime('2020-1-1', '%Y-%m-%d'))
	end = col3.date_input('End')
	
	
	if col1.button("submit"):
		df = generate_stock(symbol,start, end)
	
	graph = col4.selectbox('Choose Chart',('Lines', 'Candlestick'))
	if graph == 'Lines':
		#tipo = col2.selectbox('Output',('Volume','Prices'))
		
		
		df = generate_stock(symbol,start, end)
		df['SMA'] = df['Close'].rolling(window = 20).mean()
		df['EMA'] = df['Close'].ewm(span=21,adjust = False).mean()
		df['STD'] = df['Close'].rolling(window = 20).std()
		df['Upper'] = df['SMA'] + (df['STD']*2) #UPPER
		df['Lower'] = df['SMA'] - (df['STD']*2) #LOWER
		df['MACD'] = df['Close'].ewm(span=12,adjust = False).mean() - df['Close'].ewm(span=26,adjust = False).mean() 
		df['SIGNAL'] = df['MACD'].ewm(span = 9, adjust = False).mean()
		delta = df['Adj Close'].diff(1)
		delta = delta.dropna()
		up = delta.copy()
		down = delta.copy()
		up[up<0] = 0
		down[down>0] = 0	
		col1.subheader('')
		AVG_gain = up.rolling(window = 14).mean()
		AVG_loss = abs(down.rolling(window = 14).mean())
		RS = AVG_gain /AVG_loss
		RSI = 100 - (100/(1+RS))	

		op = col1.checkbox('Open Prince')
		cl = col1.checkbox('Close Price')
		smv = col1.checkbox('Simple Moving Average')
		emv = col1.checkbox('Exponencial Moving Average')
		bol = col1.checkbox('Bolinger Bands')
		fig1 = go.Figure()
		if cl:
			close()
		if op:
			Open()
		if smv:
			SMA()
		if emv:
			EMA()
		if bol:
			upper()
			lower()

			
		fig1.update_layout(xaxis_rangeslider_visible=True,  showlegend=False)
		
		col2.plotly_chart(fig1, use_column_width=True)
		
		col1.subheader('')
		col1.subheader('')
		col1.subheader('')	
		col1.subheader('')	
		col1.subheader('')	
		col1.subheader('')
		col1.subheader('Indicators')
					
		indicators = col1.selectbox('Choose Indicator',('Volume', 'RSI','MACD'))
		
		if indicators == 'Volume':
			
			fig2 = px.area(df, x = df.index, y = 'Volume',title=symbol)
			fig2.update_layout(xaxis_rangeslider_visible=True)
			col2.plotly_chart(fig2)

		if indicators == 'RSI':
			
			fig3 = go.Figure()
			fig3.add_trace(go.Scatter(x=RSI.index, y=RSI.values, mode='lines',line=dict(color='gray'), name = 'RSI'))
			fig3.update_layout(xaxis_rangeslider_visible=True)
			col2.plotly_chart(fig3,use_column_width=True)

		if indicators == 'MACD':
			
			fig4 = go.Figure()
			fig4.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines',line=dict(color='red'), name = 'MACD'))
			fig4.add_trace(go.Scatter(x=df.index, y=df['SIGNAL'], mode='lines',line=dict(color='blue'), name = 'SIGNAL LINE'))
			fig4.update_layout(xaxis_rangeslider_visible=True)
			col2.plotly_chart(fig4,use_column_width=True)




			
	if graph == 'Candlestick':
		df = generate_stock(symbol,start, end)
		df['SMA'] = df['Close'].rolling(window = 20).mean()
		df['EMA'] = df['Close'].ewm(span=21,adjust = False).mean()
		df['STD'] = df['Close'].rolling(window = 20).std()
		df['Upper'] = df['SMA'] + (df['STD']*2) #UPPER
		df['Lower'] = df['SMA'] - (df['STD']*2)
		df['MACD'] = df['Close'].ewm(span=12,adjust = False).mean() - df['Close'].ewm(span=26,adjust = False).mean() 
		df['SIGNAL'] = df['MACD'].ewm(span = 9, adjust = False).mean()

		col1.subheader('')	
		col1.subheader('')
		
		bol = col1.checkbox('Bolinger Bands')
		smv = col1.checkbox('Simple Moving Average')
		emv = col1.checkbox('Exponencial Moving Average')
		fig1 = go.Figure(data = [go.Candlestick(x= df.index,
			                            close= df['Close'],
			                            high = df['High'],
			                            low = df['Low'],
			                            open = df['Open'],                 
			                            increasing_line_color = 'green',
			                            decreasing_line_color = 'red')])

		fig1.update_layout(xaxis_rangeslider_visible=True,  showlegend=False)
		if smv:
			SMA()
		if emv:
			EMA()
		if bol:
			upper()
			lower()
		col2.plotly_chart(fig1)

		col1.subheader('')
		col1.subheader('')
		col1.subheader('')	
		col1.subheader('')	
		col1.subheader('')	
		col1.subheader('')
		col1.subheader('Indicators')
		col1.subheader('')			
		indicators = col1.selectbox('Choose Indicator',('Volume', 'RSI','MACD'))
		
		if indicators == 'Volume':
			
			fig2 = px.area(df, x = df.index, y = 'Volume',title=symbol)
			fig2.update_layout(xaxis_rangeslider_visible=True)
			col2.plotly_chart(fig2)

		if indicators == 'RSI':
			
			fig3 = go.Figure()
			fig3.add_trace(go.Scatter(x=df.index, y=df['Volume'], mode='lines',line=dict(color='blue'), name = 'Volume'))
			fig3.update_layout(xaxis_rangeslider_visible=True)
			col2.plotly_chart(fig3,use_column_width=True)

		if indicators == 'MACD':
			
			fig4 = go.Figure()
			fig4.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines',line=dict(color='red'), name = 'MACD'))
			fig4.add_trace(go.Scatter(x=df.index, y=df['SIGNAL'], mode='lines',line=dict(color='blue'), name = 'SIGNAL LINE'))
			fig4.update_layout(xaxis_rangeslider_visible=True)
			col2.plotly_chart(fig4,use_column_width=True)




if nav == "Statistics":
	token = gt()
	st.header('Statistics')
	col1 , col2 = st.beta_columns(2)
	symbol = col1.text_input ('Enter symbol','AMZN')
	if col1.button("submit"):
		valuation_measures,balance_sheet, income_statement = statistics(symbol)
	
		#st.title('Statistics')
	fn = col2.selectbox('Choose statistics',('Valuation Measures', 'Balance Sheet','Income Statement'))
	if fn == 'Valuation Measures':
		
		valuation_measures,balance_sheet, income_statement = statistics(symbol)
		st.subheader('Valuation Measures')
		st.write(valuation_measures)
	if fn == 'Balance Sheet':
		
		valuation_measures,balance_sheet, income_statement = statistics(symbol)
		st.subheader('Balance Sheet')
		st.write(balance_sheet)
	if fn == 'Income Statement':
		valuation_measures,balance_sheet, income_statement = statistics(symbol)
		st.subheader('Income Statement')
		st.write(income_statement)
	
if nav == "Market Live":
	token = gt()
	st.header('Market Live')
	col1 , col2, col3,col4 = st.beta_columns(4)
	symbol = col1.text_input ('Enter symbol','FB')
	col2.subheader('')
	df = live(symbol)
	if col2.button('Update'):
		df = live(symbol)
			
	col4.subheader('')
	last = df['close'][-1]
	col4.info(f'Price ${last}')
	col3.subheader('')		
			
	#col3.info('Ganancia')
					#col2.info(f" Last Price {get_last(symbols=symbol, token = token)[0]['price']}")

				#df = generate_stock(symbol,'2020-01-01', '2020-10-01')
				#time.sleep(5)

	df['SMA'] = df['close'].rolling(window = 20).mean()
	df['EMA'] = df['close'].ewm(span=21,adjust = False).mean()
	df['STD'] = df['close'].rolling(window = 20).std()
	df['Upper'] = df['SMA'] + (df['STD']*2) #UPPER
	df['Lower'] = df['SMA'] - (df['STD']*2)
		#df['MACD'] = df['close'].ewm(span=12,adjust = False).mean() - df['Close'].ewm(span=26,adjust = False).mean() 
		#df['SIGNAL'] = df['MACD'].ewm(span = 9, adjust = False).mean()
			
				
	bol = col1.checkbox('Bolinger Bands')
	smv = col1.checkbox('Simple Moving Average')
	emv = col1.checkbox('Exponencial Moving Average')
	points = col1.checkbox('Show points')
	enter = col1.number_input('Enter point')
	stop = col1.number_input('Stop loss')
	ganancia = round(ganancia(last, enter),2)
	

	fig1 = go.Figure(data = [go.Candlestick(x= df.index,
						                            close= df['close'],
						                            high = df['high'],
						                            low = df['low'],
						                            open = df['open'],                 
						                            increasing_line_color = 'green',
						                            decreasing_line_color = 'red')])

	fig1.update_layout(xaxis_rangeslider_visible=True,  showlegend=False)
	if smv:
		SMA()
	if emv:
		EMA()
	if bol:
		upper()
		lower()
	if points:
		p_ent(enter)
		p_stop(stop)
		col3.info(f'{ganancia} %')
	col2.plotly_chart(fig1)




	
	
	

if nav == "News Paper":
	token = gt()
	col1 , col2= st.beta_columns([4,1])
	col1.header('News Paper')

	
	source = col1.selectbox('Choose Source',('Washington Post', 'New York Times', 'El Universal'))
	col2.subheader('')
	col2.subheader('')
	
	#sec = col2.selectbox('Choose Seccion',('Bussines', 'Politics','World', 'Markets', 'Tech', 'Sports', 'Coronavirus'))
	if source == 'Washington Post':
		sec = col2.selectbox('Choose Seccion',('Bussines', 'Politics','World', 'Markets', 'Tech', 'Sports', 'Coronavirus'))
		if sec == 'Bussines':
			url = 'https://www.washingtonpost.com/business/?itid=nb_front_business'
			links = news(url)
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
				

					if col1.button('Download PDF ' + str(i+1)):
						
						texto_n = [i.replace('\n\nAD\n','') for i in article.text.split(' ')]
						texto = ' '.join(texto_n)
						f=open(f"{article.title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/wh.png', 0,0,60,15)
						#pdf.titles('probando')
						pdf.texts(f"{article.title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass
					

		if sec == 'Politics':
			url = 'https://www.washingtonpost.com/politics/?itid=nb_front_politics'
			links = news(url)
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])

					if col1.button('Download PDF ' + str(i+1)):
						
						texto_n = [i.replace('\n\nAD\n','') for i in article.text.split(' ')]
						texto = ' '.join(texto_n)
						f=open(f"{article.title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/wh.png', 0,0,60,15)
						#pdf.titles('probando')
						pdf.texts(f"{article.title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass

		if sec == 'World':
			url = 'https://www.washingtonpost.com/world/?itid=nb_front_world'
			links = news(url)
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])

					if col1.button('Download PDF ' + str(i+1)):
						
						texto_n = [i.replace('\n\nAD\n','') for i in article.text.split(' ')]
						texto = ' '.join(texto_n)
						f=open(f"{article.title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/wh.png', 0,0,60,15)
						#pdf.titles('probando')
						pdf.texts(f"{article.title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass

		if sec == 'Markets':
			url = 'https://www.washingtonpost.com/markets/?itid=nb_front_business_markets'
			links = news(url)
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])

					if col1.button('Download PDF ' + str(i+1)):
						
						texto_n = [i.replace('\n\nAD\n','') for i in article.text.split(' ')]
						texto = ' '.join(texto_n)
						f=open(f"{article.title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/wh.png', 0,0,60,15)
						#pdf.titles('probando')
						pdf.texts(f"{article.title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass


		if sec == 'Tech':
			url = 'https://www.washingtonpost.com/business/technology/?itid=nb_front_technology'
			links = news(url)
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])

					if col1.button('Download PDF ' + str(i+1)):
						
						texto_n = [i.replace('\n\nAD\n','') for i in article.text.split(' ')]
						texto = ' '.join(texto_n)
						f=open(f"{article.title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/wh.png', 0,0,60,15)
						#pdf.titles('probando')
						pdf.texts(f"{article.title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass

		if sec == 'Sports':
			url = 'https://www.washingtonpost.com/sports/?itid=nb_front_sports'
			links = news(url)
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])


					if col1.button('Download PDF ' + str(i+1)):
						
						texto_n = [i.replace('\n\nAD\n','') for i in article.text.split(' ')]
						texto = ' '.join(texto_n)
						f=open(f"{article.title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/wh.png', 0,0,60,15)
						#pdf.titles('probando')
						pdf.texts(f"{article.title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass

		if sec == 'Coronavirus':
			url = 'https://www.washingtonpost.com/coronavirus/?itid=nb_front_coronavirus'
			links = news(url)
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])


					if col1.button('Download PDF ' + str(i+1)):
						
						texto_n = [i.replace('\n\nAD\n','') for i in article.text.split(' ')]
						texto = ' '.join(texto_n)
						f=open(f"{article.title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/wh.png', 0,0,60,15)
						#pdf.titles('probando')
						pdf.texts(f"{article.title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass

	if source == 'New York Times':
		sec = col2.selectbox('Choose Seccion',('Bussines', 'World', 'Politics', 'Tech', 'Sports', 'Opinion'))
		if sec == 'Bussines':
			url = 'https://www.nytimes.com/section/business'
			links = news(url)
			links = ['https://www.nytimes.com' +i for i in links ]
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
					if col1.button('Download PDF ' + str(i+1)):
						
						title = [i.replace("’", '') for i in article.title.split(' ')]
						title = ' '.join(title)
						texto = [i.replace("’", '') for i in article.text.split(' ')]
						texto = ' '.join(texto)
						title = title + '\n\n'
						texto = title + texto
						f=open(f"{title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/ny.png', 0,0,60,15)
						#pdf.titles('PRUEBA')
						pdf.texts(f"{title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass



		if sec == 'World':
			url = 'https://www.nytimes.com/section/world'
			links = news(url)
			links = ['https://www.nytimes.com' +i for i in links ]
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
					if col1.button('Download PDF ' + str(i+1)):
						
						title = [i.replace("’", '') for i in article.title.split(' ')]
						title = ' '.join(title)
						texto = [i.replace("’", '') for i in article.text.split(' ')]
						texto = ' '.join(texto)
						title = title + '\n\n'
						texto = title + texto
						f=open(f"{title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/ny.png', 0,0,60,15)
						#pdf.titles('PRUEBA')
						pdf.texts(f"{title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass


		if sec == 'Politics':
			url = 'https://www.nytimes.com/section/politics'
			links = news(url)
			links = ['https://www.nytimes.com' +i for i in links ]
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
					if col1.button('Download PDF ' + str(i+1)):
						
						title = [i.replace("’", '') for i in article.title.split(' ')]
						title = ' '.join(title)
						texto = [i.replace("’", '') for i in article.text.split(' ')]
						texto = ' '.join(texto)
						title = title + '\n\n'
						texto = title + texto
						f=open(f"{title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/ny.png', 0,0,60,15)
						#pdf.titles('PRUEBA')
						pdf.texts(f"{title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass


		if sec == 'Tech':
			url = 'https://www.nytimes.com/section/technology'
			links = news(url)
			links = ['https://www.nytimes.com' +i for i in links ]
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
					if col1.button('Download PDF ' + str(i+1)):
						
						title = [i.replace("’", '') for i in article.title.split(' ')]
						title = ' '.join(title)
						texto = [i.replace("’", '') for i in article.text.split(' ')]
						texto = ' '.join(texto)
						title = title + '\n\n'
						texto = title + texto
						f=open(f"{title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/ny.png', 0,0,60,15)
						#pdf.titles('PRUEBA')
						pdf.texts(f"{title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')


			except:
				pass


		if sec == 'Sports':
			url = 'https://www.nytimes.com/section/sports'
			links = news(url)
			links = ['https://www.nytimes.com' +i for i in links ]
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
					if col1.button('Download PDF ' + str(i+1)):
						
						title = [i.replace("’", '') for i in article.title.split(' ')]
						title = ' '.join(title)
						texto = [i.replace("’", '') for i in article.text.split(' ')]
						texto = ' '.join(texto)
						title = title + '\n\n'
						texto = title + texto
						f=open(f"{title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/ny.png', 0,0,60,15)
						#pdf.titles('PRUEBA')
						pdf.texts(f"{title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass


		if sec == 'Opinion':
			url = 'https://www.nytimes.com/section/opinion'
			links = news(url)
			links = ['https://www.nytimes.com' +i for i in links ]
			try:
				for i in range(0,len(links)):
				
					article = art(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
					if col1.button('Download PDF ' + str(i+1)):
						
						title = [i.replace("’", '') for i in article.title.split(' ')]
						title = ' '.join(title)
						texto = [i.replace("’", '') for i in article.text.split(' ')]
						texto = ' '.join(texto)
						title = title + '\n\n'
						texto = title + texto
						f=open(f"{title}.txt","w", encoding="utf-8")
						f.write(texto)
						f.close()
						pdf = PDF()
						pdf.add_page()
						pdf.logo('img/ny.png', 0,0,60,15)
						#pdf.titles('PRUEBA')
						pdf.texts(f"{title}.txt")
						pdf.set_author('iván serrano')
						pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass

	if source == 'El Universal':
		sec3 = col2.selectbox('Choose Seccion',('Nación', 'Mundo','Metrópoli', 'Estados', 'Cartera', 'Deportes'))

		if sec3 == 'Nación':
			url = 'https://www.eluniversal.com.mx/nacion'
			links = universal(url)
			try:
				for i in range(0,len(links)):
				
					article = art_es(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
					if col1.button('Download PDF ' + str(i+1)):
						title = article.title + '\n\n'
						texto = title + article.text
						try:
							f=open(f"{article.title}.txt","w", encoding="latin-1")
							f.write(texto)
							f.close()
							pdf = PDF()
							pdf.add_page()
							pdf.logo('universal.png', 0,0,60,20)
							#pdf.titles('PRUEBA')
							pdf.texts(f"{article.title}.txt")
							pdf.set_author('iván serrano')
							pdf.output(f'{article.title}.pdf', 'F')
						except:
							f=open(f"{article.title}.txt","w", encoding="utf-8")
							f.write(texto)
							f.close()
							pdf = PDF()
							pdf.add_page()
							pdf.logo('img/universal.png', 0,0,60,20)
							#pdf.titles('PRUEBA')
							pdf.texts(f"{article.title}.txt")
							pdf.set_author('iván serrano')
							pdf.output(f'{article.title}.pdf', 'F')

			except:
				pass
		
		if sec3 == 'Mundo':
			url = 'https://www.eluniversal.com.mx/mundo'
			links = universal2(url)
			try:
				for i in range(0,len(links)):
				
					article = art_es(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
					if col1.button('Download PDF ' + str(i+1)):
						title = article.title + '\n\n'
						texto = title + article.text
						try:
							f=open(f"{article.title}.txt","w", encoding="latin-1")
							f.write(texto)
							f.close()
							pdf = PDF()
							pdf.add_page()
							pdf.logo('universal.png', 0,0,60,20)
							#pdf.titles('PRUEBA')
							pdf.texts(f"{article.title}.txt")
							pdf.set_author('iván serrano')
							pdf.output(f'{article.title}.pdf', 'F')
						except:
							f=open(f"{article.title}.txt","w", encoding="utf-8")
							f.write(texto)
							f.close()
							pdf = PDF()
							pdf.add_page()
							pdf.logo('img/universal.png', 0,0,60,20)
							#pdf.titles('PRUEBA')
							pdf.texts(f"{article.title}.txt")
							pdf.set_author('iván serrano')
							pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass		

		if sec3 == 'Metrópoli':
			url = 'https://www.eluniversal.com.mx/metropoli'
			links = universal2(url)
			try:
				for i in range(0,len(links)):
				
					article = art_es(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
					if col1.button('Download PDF ' + str(i+1)):
						title = article.title + '\n\n'
						texto = title + article.text
						try:
							f=open(f"{article.title}.txt","w", encoding="latin-1")
							f.write(texto)
							f.close()
							pdf = PDF()
							pdf.add_page()
							pdf.logo('universal.png', 0,0,60,20)
							#pdf.titles('PRUEBA')
							pdf.texts(f"{article.title}.txt")
							pdf.set_author('iván serrano')
							pdf.output(f'{article.title}.pdf', 'F')
						except:
							f=open(f"{article.title}.txt","w", encoding="utf-8")
							f.write(texto)
							f.close()
							pdf = PDF()
							pdf.add_page()
							pdf.logo('img/universal.png', 0,0,60,20)
							#pdf.titles('PRUEBA')
							pdf.texts(f"{article.title}.txt")
							pdf.set_author('iván serrano')
							pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass



		if sec3 == 'Estados':
			url = 'https://www.eluniversal.com.mx/estados'
			links = universal2(url)
			links = links[1:]
			try:
				for i in range(0,len(links)):
				
					article = art_es(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
					if col1.button('Download PDF ' + str(i+1)):
						title = article.title + '\n\n'
						texto = title + article.text
						try:
							f=open(f"{article.title}.txt","w", encoding="latin-1")
							f.write(texto)
							f.close()
							pdf = PDF()
							pdf.add_page()
							pdf.logo('img/universal.png', 0,0,60,20)
							#pdf.titles('PRUEBA')
							pdf.texts(f"{article.title}.txt")
							pdf.set_author('iván serrano')
							pdf.output(f'{article.title}.pdf', 'F')
						except:
							f=open(f"{article.title}.txt","w", encoding="utf-8")
							f.write(texto)
							f.close()
							pdf = PDF()
							pdf.add_page()
							pdf.logo('universal.png', 0,0,60,20)
							#pdf.titles('PRUEBA')
							pdf.texts(f"{article.title}.txt")
							pdf.set_author('iván serrano')
							pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass


		if sec3 == 'Cartera':
			url = 'https://www.eluniversal.com.mx/cartera'
			links = universal2(url)
			base = 'https://www.eluniversal.com.mx/'
			links = [base + i for i in links if base not in i]
			try:
				for i in range(0,len(links)):
				
					article = art_es(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
					if col1.button('Download PDF ' + str(i+1)):
						title = article.title + '\n\n'
						texto = title + article.text
						try:
							f=open(f"{article.title}.txt","w", encoding="latin-1")
							f.write(texto)
							f.close()
							pdf = PDF()
							pdf.add_page()
							pdf.logo('img/universal.png', 0,0,60,20)
							#pdf.titles('PRUEBA')
							pdf.texts(f"{article.title}.txt")
							pdf.set_author('iván serrano')
							pdf.output(f'{article.title}.pdf', 'F')
						except:
							f=open(f"{article.title}.txt","w", encoding="utf-8")
							f.write(texto)
							f.close()
							pdf = PDF()
							pdf.add_page()
							pdf.logo('universal.png', 0,0,60,20)
							#pdf.titles('PRUEBA')
							pdf.texts(f"{article.title}.txt")
							pdf.set_author('iván serrano')
							pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass



		if sec3 == 'Deportes':
			url = 'https://www.eluniversal.com.mx/deportes'
			links = universal2(url)
			try:
				for i in range(0,len(links)):
				
					article = art_es(links[i])
					col1.info(article.title)
					col1.text(article.summary)
					col1.text(f'Date {article.publish_date.date()}')
					col1.info(links[i])
					if col1.button('Download PDF ' + str(i+1)):
						title = article.title + '\n\n'
						texto = title + article.text
						try:
							f=open(f"{article.title}.txt","w", encoding="latin-1")
							f.write(texto)
							f.close()
							pdf = PDF()
							pdf.add_page()
							pdf.logo('img/universal.png', 0,0,60,20)
							#pdf.titles('PRUEBA')
							pdf.texts(f"{article.title}.txt")
							pdf.set_author('iván serrano')
							pdf.output(f'{article.title}.pdf', 'F')
						except:
							f=open(f"{article.title}.txt","w", encoding="utf-8")
							f.write(texto)
							f.close()
							pdf = PDF()
							pdf.add_page()
							pdf.logo('universal.png', 0,0,60,20)
							#pdf.titles('PRUEBA')
							pdf.texts(f"{article.title}.txt")
							pdf.set_author('iván serrano')
							pdf.output(f'{article.title}.pdf', 'F')
			except:
				pass


if nav == "Market Simulator":
	token = gt()
	col1 , col2 = st.beta_columns([4,1])
	col1.header('Market Simulator')
	col2.subheader('')
	col1.subheader('')

	with col1.beta_expander('Board 1', expanded=True):
		symbol = st.text_input ('Enter Symbol 1','AMZN')
		if st.checkbox('Start 1'):
		    with st.empty():
		        for seconds in range(60):
		            st.info("updated")
		            st.plotly_chart(candle_intra(live(symbol)),use_container_width=True)
		            time.sleep(10)
		else:
			st.plotly_chart(candle_intra(live(symbol)),use_container_width=True)

	with col1.beta_expander('Board 2'):
		symbol = st.text_input ('Enter Symbol 2','FB')
		if st.checkbox('Start 2'):
		    with st.empty():
			    for seconds in range(60):
			        st.info("updated")
			        st.plotly_chart(candle_intra(live(symbol)))
			        time.sleep(10)
		else:
			st.plotly_chart(candle_intra(live(symbol)),use_container_width=True)

	with col1.beta_expander('Board 3'):
		symbol = st.text_input ('Enter Symbol 3','AAPL')
		if st.checkbox('Start 3'):
		    with st.empty():
		        for seconds in range(60):
		            st.info("updated")
		            st.plotly_chart(candle_intra(live(symbol)))
		            time.sleep(10)
		else:
			st.plotly_chart(candle_intra(live(symbol)),use_container_width=True)

	col2.subheader('')
	col2.subheader('')

	with col2.beta_expander('Board 1',expanded=True):
	    symbol = st.text_input ('Symbol 1','AMZN')
	    if st.checkbox('start 1'):
	        st.subheader('')
	        st.subheader('')
	        st.subheader('') 
	        with st.empty():
	            for seconds in range(60):
	                last = live(symbol)['close'][-1]
	                avg =  live(symbol)['average'][-1]
	                hour = live(symbol)['label'][-1]
	                st.subheader('')
	                st.subheader('')
	                st.subheader('')
	                st.write("Price:",
	                    round(last,2),
	                    "Avg:",
	                    round(last,2),
	                    "Hour:",
	                    hour)
	                time.sleep(10)
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.text('')
	    else:            
	        df = live(symbol)
	        last = df['close'][-1]
	        average = df['average']
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        df = live(symbol)
	        last = df['close'][-1]
	        avg =  df['average'][-1]
	        hour = df['label'][-1]
	        st.write("Price:",
	                    round(last,2),
	                    "Avg:",
	                    round(avg,2),
	                    "Hour:",
	                    hour)
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.text('')      

	with col2.beta_expander('Board 2'):
	    symbol = st.text_input ('Symbol 2','FB')
	    if st.checkbox('start 2'):
	        st.subheader('')
	        st.subheader('')
	        st.subheader('') 
	        with st.empty():
	            for seconds in range(60):
	                last = live(symbol)['close'][-1]
	                avg =  live(symbol)['average'][-1]
	                hour = live(symbol)['label'][-1]
	                st.subheader('')
	                st.subheader('')
	                st.subheader('')
	                st.write("Price:",
	                    round(last,2),
	                    "Avg:",
	                    round(last,2),
	                    "Hour:",
	                    hour)
	                time.sleep(10)
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.text('')
	    else:            
	        df = live(symbol)
	        last = df['close'][-1]
	        average = df['average']
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        df = live(symbol)
	        last = df['close'][-1]
	        avg =  df['average'][-1]
	        hour = df['label'][-1]
	        st.write("Price:",
	                    round(last,2),
	                    "Avg:",
	                    round(avg,2),
	                    "Hour:",
	                    hour)
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.text('')
	with col2.beta_expander('Board 3'):
	    symbol = st.text_input ('Symbol 3','AAPL')
	    if st.checkbox('start 3'):
	        st.subheader('')
	        st.subheader('')
	        st.subheader('') 
	        with st.empty():
	            for seconds in range(60):
	                last = live(symbol)['close'][-1]
	                avg =  live(symbol)['average'][-1]
	                hour = live(symbol)['label'][-1]
	                st.subheader('')
	                st.subheader('')
	                st.subheader('')
	                st.write("Price:",
	                    round(last,2),
	                    "Avg:",
	                    round(last,2),
	                    "Hour:",
	                    hour)
	                time.sleep(10)
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.text('')
	    else:            
	        df = live(symbol)
	        last = df['close'][-1]
	        average = df['average']
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        df = live(symbol)
	        last = df['close'][-1]
	        avg =  df['average'][-1]
	        hour = df['label'][-1]
	        st.write("Price:",
	                    round(last,2),
	                    "Avg:",
	                    round(avg,2),
	                    "Hour:",
	                    hour)
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.subheader('')
	        st.text('')






	



