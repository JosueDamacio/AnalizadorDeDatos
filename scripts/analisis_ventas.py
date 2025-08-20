
import pandas as pd
import os

#leo los datos de ventas desde el archivo csv
df_ventas = pd.read_csv("analisis/datos/ventas_ecomerce_1.csv")

#me aseguro de que la carpeta de resultados exista
carpeta_resultados = "analisis/resultados"
os.makedirs(carpeta_resultados, exist_ok=True)

resumenes = []




#productos con más ventas
top_vendidos = df_ventas.sort_values("cantidad_vendida", ascending=False).head(5)
resumenes.append("=====Productos más vendidos=====\n" + top_vendidos[["producto", "cantidad_vendida"]].to_string(index=False))


#productos con mayor stock disponible
top_stock = df_ventas.sort_values("stock", ascending=False).head(5)
resumenes.append("=====Productos con más stock=====\n" + top_stock[["producto", "stock"]].to_string(index=False))


#ingreso total por producto (precio por cantidad)
df_ventas["ingreso_total"] = df_ventas["precio"] * df_ventas["cantidad_vendida"]
top_ingresos = df_ventas.sort_values("ingreso_total", ascending=False).head(5)
resumenes.append("=====Ingreso total (precio x cant)=====\n" + top_ingresos[["producto", "ingreso_total"]].to_string(index=False))


#margen de ganancia unitario
df_ventas["margen_ganancia"] = df_ventas["precio"] - df_ventas["costo"]
top_margen = df_ventas.sort_values("margen_ganancia", ascending=False).head(5)
resumenes.append("=====Productos con mayor margen de ganancia (unitario)=====\n" + top_margen[["producto", "margen_ganancia"]].to_string(index=False))


#rotación de inventario, cuidado con divisiones por cero
df_ventas["rotacion_inventario"] = df_ventas["ventas_mes"] / df_ventas["stock"].replace(0, 1)
top_rotacion = df_ventas.sort_values("rotacion_inventario", ascending=False).head(5)
resumenes.append("=====Productos con mayor rotación de inventario=====\n" + top_rotacion[["producto", "rotacion_inventario"]].to_string(index=False))


#productos con más ventas este mes
top_mes = df_ventas.sort_values("ventas_mes", ascending=False).head(5)
resumenes.append("=====Productos con más ventas este mes=====\n" + top_mes[["producto", "ventas_mes"]].to_string(index=False))


#ventas totales agrupadas por canal
ventas_por_canal = df_ventas.groupby("canal")["cantidad_vendida"].sum().sort_values(ascending=False)
resumenes.append("=====Ventas totales por canal=====\n" + ventas_por_canal.to_string())


#productos con mayor ticket promedio
top_ticket = df_ventas.sort_values("ticket_promedio", ascending=False).head(5)
resumenes.append("=====Productos con mayor ticket promedio=====\n" + top_ticket[["producto", "ticket_promedio"]].to_string(index=False))


#tasa de devolución, cuidado con divisiones por cero
df_ventas["tasa_devolucion"] = df_ventas["devoluciones"] / df_ventas["cantidad_vendida"].replace(0, 1)
top_devoluciones = df_ventas.sort_values("tasa_devolucion", ascending=False).head(5)
resumenes.append("=====Productos con mayor tasa de devolución=====\n" + top_devoluciones[["producto", "tasa_devolucion"]].to_string(index=False))


#ventas agrupadas por campaña
ventas_por_camp = df_ventas.groupby("campaña")["cantidad_vendida"].sum().sort_values(ascending=False)
resumenes.append("=====Ventas totales por campaña=====\n" + ventas_por_camp.to_string())


#productos mejor calificados
top_calificados = df_ventas.sort_values("calificacion", ascending=False).head(5)
resumenes.append("=====Productos mejor calificados=====\n" + top_calificados[["producto", "calificacion"]].to_string(index=False))


#productos con ventas más recientes
df_ventas["fecha_ultima_venta"] = pd.to_datetime(df_ventas["fecha_ultima_venta"])
top_recientes = df_ventas.sort_values("fecha_ultima_venta", ascending=False).head(5)
resumenes.append("=====Productos con ventas más recientes=====\n" + top_recientes[["producto", "fecha_ultima_venta"]].to_string(index=False))



# Consejos automáticos basados en reglas de negocio
consejos = []
for _, row in df_ventas.iterrows():
	# Consejo sobre stock alto y baja rotación
	if row['stock'] > 30 and row['rotacion_inventario'] < 0.5:
		consejos.append(f"{row['producto']}: Alto stock y baja rotación. Sugerencia: lanzar promoción o rebaja para evitar sobrestock.")
	# Consejo sobre alta tasa de devolución
	if row['tasa_devolucion'] > 0.05:
		consejos.append(f"{row['producto']}: Alta tasa de devolución ({row['tasa_devolucion']:.1%}). Sugerencia: revisar calidad, descripción o proceso de venta.")
	# Consejo sobre potencial de ventas
	if row['ventas_mes'] > df_ventas['ventas_mes'].mean() and row['margen_ganancia'] > df_ventas['margen_ganancia'].mean():
		consejos.append(f"{row['producto']}: Potencial de altas ventas y buen margen. Sugerencia: priorizar stock y campañas para este producto.")
	# Consejo sobre canal
	if row['canal'] == 'Online' and row['cantidad_vendida'] > df_ventas['cantidad_vendida'].mean():
		consejos.append(f"{row['producto']}: Buen desempeño en canal online. Sugerencia: reforzar inversión en este canal.")
	# Consejo sobre ticket promedio
	if row['ticket_promedio'] > df_ventas['ticket_promedio'].mean():
		consejos.append(f"{row['producto']}: Ticket promedio alto. Sugerencia: ofrecer bundles o ventas cruzadas para aumentar aún más el ticket.")

# Consejo general sobre campañas
ventas_camp = df_ventas.groupby("campaña")["cantidad_vendida"].sum()
campana_top = ventas_camp.idxmax()
consejos.append(f"La campaña con más ventas fue '{campana_top}'. Sugerencia: analizar qué funcionó bien y replicar estrategias similares.")

#guardo todo en el txt de resultados
with open(os.path.join(carpeta_resultados, "ventas_ecomerce_1.txt"), "w", encoding="utf-8") as f:
	f.write("\n\n".join(resumenes))
	f.write("\n\n=====Consejos automáticos=====" + ("\n" + "\n".join(consejos) if consejos else "\n(no se detectaron consejos relevantes para los datos actuales)"))
