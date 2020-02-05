## Link
- `plot3Dsurfacevector`는 자체 개발
- `Arrow3D` 객체는 아래 링크 참고
- https://stackoverflow.com/questions/22867620/putting-arrowheads-on-vectors-in-matplotlibs-3d-plot

## 어떤 역할?
- 3D 벡터가 주어졌을 때 직육면체로 이 벡터가 어느 사분면에 있는지 시각화해주는 함수
- 내가 구현~

## 코드는?
```python
import numpy as np
import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

def plot3Dsurfacevector(v, ax, orig=[0,0,0], **kwargs):
    use_dict = {'X':0, 'Y':1, 'Z':2}
    xs, ys, zs = sorted([v[0], 0]), sorted([v[1], 0]), sorted([v[2], 0])
    x, y, z = np.linspace(*xs, 100), np.linspace(*ys, 100), np.linspace(*zs, 100)
    cord_name = list(map(lambda x : x, itertools.permutations(['X', 'Y', 'Z'], 2)))
    cord_val = list(map(lambda x : x, itertools.permutations((x, y, z))))
    usage_li = []
    for name, val in zip(cord_name, cord_val):
        val_dict, coords = {}, ['X', 'Y', 'Z']
        a, b = np.meshgrid(*val[:-1])
        val_dict[name[0]], val_dict[name[1]] = a, b
        axis = [n for n in coords if n not in name][0]
        if ''.join(name[::-1]) in usage_li:
            another_coord = v[use_dict[axis]]
        else:
            another_coord = 0
        val_dict[axis] = a * 0 + another_coord
        val_dict = dict(sorted(val_dict.items(), key=lambda x : x[0]))
        surf = ax.plot_surface(**val_dict, rstride=5, cstride=5, **kwargs)
        surf._facecolors2d = surf._facecolors3d; surf._edgecolors2d = surf._edgecolors3d
        usage_li.append(''.join(name))
    a = Arrow3D([orig[0], v[0]], [orig[1], v[1]], 
                [orig[2], v[2]], mutation_scale=20, 
                lw=3, arrowstyle="-|>", alpha=1, color='k', zorder=7)
    ax.add_artist(a)
    return surf
    
fig = plt.figure(figsize=(12, 10), facecolor='w')
plt.subplots_adjust(wspace=0)

ax = plt.subplot(1, 1, 1, projection='3d')
plot3Dsurfacevector(( 2, -1, -3), ax, alpha=0.2, color='g')
plot3Dsurfacevector((-1,  2,  0), ax, alpha=0.1, color='r')
plot3Dsurfacevector(( 0, -1,  4), ax, alpha=0.1, color='b')
ax.view_init(30, 30)    
```
![title](https://github.com/jinmang2/bring_it_on/blob/master/img/3DvectorWithCuboid.png?raw=true)
