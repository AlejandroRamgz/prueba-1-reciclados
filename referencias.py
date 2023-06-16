def diccionario_colores(color): 
    colores = {
        'black' : (0,0,0), 
        'white' : (255,255,255),
        'green' : (96,218,117),
        'blue' : (96,181,218),
        'red': (239,71,71),
        'rose':(214,74,236),
        'grissoscuro':(128, 139, 150 ),
        'grisintermedio':(171, 178, 185 ),
        'grisclaro':(213, 216, 220 ),
        'grismasclaro':(234, 236, 238),
        }

    return colores[color]

def dcol_set(hoja, color):
    cr, cg, cb = diccionario_colores(color)
    hoja.set_draw_color(r= cr, g = cg, b= cb)
    
def bcol_set(hoja,color):
    cr, cg, cb = diccionario_colores(color)
    hoja.set_fill_color(r= cr, g = cg, b= cb)

def tcol_set(hoja, color):
    cr, cg, cb = diccionario_colores(color)
    hoja.set_text_color(r= cr, g = cg, b= cb)
    
def tfont_size(hoja, size):
    hoja.set_font_size(size)

def tfont(hoja, estilo, fuente='Times'):
    hoja.set_font(fuente, style=estilo)