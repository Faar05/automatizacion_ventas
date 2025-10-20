# 🏢 PRUEBA TÉCNICA - AUTOMATIZACIÓN DE VENTAS RPA

## 📋 DESCRIPCIÓN DEL PROBLEMA

En nuestra empresa manejamos archivos Excel de ventas distribuidos por diferentes regiones y necesita automatizar el proceso de consolidación y análisis de estos datos. Actualmente, el proceso manual toma horas y es propenso a errores.

## 🎯 OBJETIVO

Desarrollar una solución de automatización usando Python que:

1. **Organice automáticamente** los archivos de entrada por fecha
2. **Consolide** los datos de ventas por mes
3. **Genere reportes** con datos consolidados y rankings de productos
4. **Mantenga una estructura organizacional** clara y escalable

## 📁 ESTRUCTURA INICIAL

```
Prueba tecnica 2025/
├── Input/
│   ├── sales_central_october_2025.xlsx
│   ├── sales_central_september_2025.xlsx
│   ├── sales_north_october_2025.xlsx
│   ├── sales_north_september_2025.xlsx
│   ├── sales_sur_october_2025.xlsx
│   └── sales_sur_september_2025.xlsx
└── Output/
    └── (vacía - aquí se generarán los resultados)
```

## 📊 ESTRUCTURA DE DATOS

Cada archivo Excel contiene las siguientes columnas:
- **Date**: Fecha de la venta
- **Region**: Región de venta
- **Salesperson**: Vendedor
- **Product**: Nombre del producto
- **Quantity**: Cantidad vendida
- **UnitPrice**: Precio unitario

## 🎯 REQUERIMIENTOS TÉCNICOS

### 1. **Organización de Archivos Input**
- [ ] Crear estructura de carpetas: `Output/YYYY/MM_NombreMes/`
- [ ] Mover archivos originales a carpetas organizadas por fecha

### 2. **Procesamiento de Datos**
- [ ] Extraer mes y año del nombre de cada archivo
- [ ] Consolidar todos los archivos del mismo mes
- [ ] Calcular valor total por transacción (Quantity × UnitPrice)
- [ ] Agregar información de origen (región del archivo)

### 3. **Estructura Output**
- [ ] Crear carpetas por año y mes: `Output/YYYY/MM_NombreMes/`
- [ ] Generar archivo Excel por mes: `Ventas_Consolidadas_YYYY_MM.xlsx`

### 4. **Contenido del Archivo Excel**
- [ ] **Hoja 1 - "Datos_Consolidados"**: Todos los registros de ventas del mes
- [ ] **Hoja 2 - "Ranking_Productos"**: Ranking de productos más vendidos


## 📋 CRITERIOS DE EVALUACIÓN

### **Funcionalidad (40%)**
- ✅ Correcta lectura de archivos input
- ✅ Consolidación precisa de datos
- ✅ Generación correcta de estructura output
- ✅ Creación de archivos Excel con ambas hojas

### **Calidad del Código (25%)**
- ✅ Código limpio y bien estructurado
- ✅ Funciones bien definidas y documentadas
- ✅ Manejo adecuado de errores
- ✅ Uso eficiente de librerías

### **Robustez (20%)**
- ✅ Manejo de casos edge (archivos faltantes, formatos incorrectos)
- ✅ Validación de datos de entrada

### **Escalabilidad (15%)**
- ✅ Código reutilizable para diferentes meses/años
- ✅ Estructura que soporte múltiples regiones
- ✅ Fácil mantenimiento y extensión
- ✅ Configuración flexible

## 🧪 CASOS DE PRUEBA

### **Datos de Entrada**
- 6 archivos Excel (3 regiones × 2 meses)
- ~5 registros por archivo
- 5 productos únicos
- Fechas: Septiembre y Octubre 2025

### **Resultados Esperados**
- **Archivos organizados**: Output/2025/09_Septiembre/ y 10_Octubre/
- **Reportes generados**: Output/2025/09_Septiembre/ y 10_Octubre/
- **Total registros consolidados**: 30 (15 por mes)
- **Productos en ranking**: 5 únicos

## 📝 ENTREGABLES

1. **Script principal**: `automatizacion_ventas.py` Link del **Github**
3. **Documentación**: Comentarios en código
4. **Resultados**: Archivos Excel generados con estructura correcta


## 📊 ESTRUCTURA FINAL ESPERADA

```
Prueba tecnica 2025/
├── Input/
│   ├── sales_central_october_2025.xlsx
│   ├── sales_central_september_2025.xlsx
│   ├── sales_north_october_2025.xlsx
│   ├── sales_north_september_2025.xlsx
│   ├── sales_sur_october_2025.xlsx
│   └── sales_sur_september_2025.xlsx
├── Output/
│   └── 2025/
│       ├── 09_Septiembre/
│       │   ├── sales_central_september_2025.xlsx
│       │   ├── sales_north_september_2025.xlsx
│       │   ├── sales_sur_september_2025.xlsx
│       │   └── Ventas_Consolidadas_2025_09.xlsx
│       └── 10_Octubre/
│           ├── sales_central_october_2025.xlsx
│           ├── sales_north_october_2025.xlsx
│           ├── sales_sur_october_2025.xlsx
│           └── Ventas_Consolidadas_2025_10.xlsx
└── automatizacion_ventas.py
```

## 🏆 MÉTRICAS DE ÉXITO

- **Precisión de datos**: Sin pérdida de información
- **Estructura generada**: Conforme a especificaciones
- **Código funcional**: Ejecutable sin errores

---

**¡Buena suerte con la prueba técnica!** 🚀