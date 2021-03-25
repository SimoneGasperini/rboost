import matplotlib.colors as cols
import matplotlib.cm as cm


class ColorMapper:

  def __init__ (self, cmap_name, vmin=0., vmax=1.):

    self.cmap_name = cmap_name
    self.cmap = cm.get_cmap(name=cmap_name)

    self.vmin = vmin
    self.vmax = vmax
    self.norm = cols.Normalize(vmin=vmin, vmax=vmax)

  def float2rgba (self, val):

    rgba_color = self.cmap(self.norm(val))

    return rgba_color

  def float2hex (self, val):

    rgb_color = self.float2rgba(val)[:3]
    hex_color = cols.rgb2hex(rgb_color)

    return hex_color
