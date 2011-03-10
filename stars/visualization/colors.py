from collections import namedtuple
class Color(namedtuple('Color',['red','green','blue','alpha'])):
    """
    Abstract representation of a color

    Parameters
    ----------
    red   -- int -- within the range [0, 255] (including both ends), defaults to 0
    green -- int -- within the range [0, 255] (including both ends), defaults to 0
    blue  -- int -- within the range [0, 255] (including both ends), defaults to 0
    alpha -- int -- within the range [0, 255] (including both ends), defaults to 255 (fully opaque)
    """
    def __new__(cls,red=0,green=0,blue=0,alpha=255):
        try:
            assert red>=0 and red<= 255
            assert green>=0 and green<= 255
            assert blue>=0 and blue<= 255
            assert alpha>=0 and alpha<= 255
        except AssertionError:
            raise ValueError, "(%r,%r,%r,%r) Does not appear to be a valid color."%(red,green,blue,alpha)
        return super(Color, cls).__new__(cls,red,green,blue,alpha)
        
    @classmethod
    def fromHexString(cls,s):
        """
        Return a Color instance from the Hex string.
        Supports the Following formats....
        "RGB"
        "RGBA"
        "RRGGBB"
        "RRGGBBAA"
        Will drop the "#" if it's includes, so "#rrggbb" is ok.

        Parameters
        ----------
        s -- str -- A Hex Color String.

        Example
        -------
        >>> colors = ["#f0f", "f0f", "f0fc", "ff00ff", "FF00FFCC"]
        >>> [Color.fromHexString(s).colors for s in colors]
        """
        alpha = 255
        if s.startswith('#'): # "#ff00ff" -> "ff00ff"
            s = s[1:]
        if len(s) == 3: # "FFF"
            r,g,b = [int(2*x,16) for x in s]
        elif len(s) == 4: # "FFF0" w/ Alpha
            r,g,b = [int(2*x,16) for x in s[:-1]]
            alpha = int(2*s[-1],16)
        elif len(s) == 6: # "ff00ff"
            r,g,b = [int(s[i:i+2],16) for i in xrange(0,6,2)]
        elif len(s) == 8: # "ff00ffcc" w/ Alpha
            r,g,b = [int(s[i:i+2],16) for i in xrange(0,6,2)]
            alpha = int(s[-2:],16)
        else:
            raise ValueError, 'Could not parse "%s", it does not appear to be a well formated color value.'%s
        return cls(r,g,b,alpha)
            
        
class ColorScheme(list):
    """
    Abstract representation of a Color Scheme

    Parameters
    ----------
    colors -- list -- A list of Colors.
    """
    def __init__(self, colors):
        _colors = []
        for c in colors:
            if not isinstance(c,Color):
                if issubclass(type(c),basestring):
                    c = Color.fromHexString(c) #Allow Error to raise if bad color.
                else:
                    c = Color(*c)
            _colors.append(c)
        list.__init__(self,_colors)
    def __getitem__(self,key):
        """
        Add basic support for colorSchemes that don't contain enough colors to a match a given classifcation scheme.
        With return blank (blank and transparent) colors instead of raising an error.
        """
        try:
            return list.__getitem__(self,key)
        except IndexError:
            if type(key) == int:
                return Color(alpha=0) #return an empty color
            elif type(key) == slice:
                return [self.__getitem__(x) for x in range(key.start,key.stop,key.step)]

def fade(k=1, left=(255,128,0), right=(0,255,0), background=(0,0,1), borders=(0,0,0)):
    colors = []
    if k == 1:
        #just return averages
        sr,sg,sb = [(r-l)/(2) for r,l in zip(right,left)]
        r, g, b = left
        r += sr
        g += sg
        b += sb
    else:
        #step
        sr,sg,sb = [(r-l)/(k-1) for r,l in zip(right,left)]
        r, g, b = left
    colors.append((r,g,b))
    for i in xrange(1,k-1):
        r += sr
        g += sg
        b += sb
        colors.append((r,g,b))
    colors.append(right)
    return ColorScheme(colors)

