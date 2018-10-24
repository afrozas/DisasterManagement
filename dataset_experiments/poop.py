from math import pi

from bokeh.io import output_file, show, curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import figure

output_file("pie.html")

source = ColumnDataSource(data=dict(
    start=[0, 0.2], end=[0.2, 2*pi], color=['firebrick', 'navy']
))

plot = figure()
plot.wedge(x=0, y=0, start_angle='start', end_angle='end', radius=1,
        color='color', alpha=0.6, source=source)

slider = Slider(start=.1, end=1., value=.2, step=.1, title="delta-V")

def update(source=source, slider=slider, window=None):
    data = source.data
    data['end'][0] = slider.value
    source.trigger('change')

slider.js_on_change('value', CustomJS.from_py_func(update))

show(column(slider, plot))
curdoc().title = "MR. POOPY BUTTHOLE"
curdoc().add_root(fig)
server.io_loop.start()
