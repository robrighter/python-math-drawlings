import vsketch
import math

class VskTestSketch(vsketch.SketchClass):
    # Sketch parameters:
    period = vsketch.Param(200)
    amplitude = vsketch.Param(40)
    frequency = vsketch.Param(2)
    interval = vsketch.Param(1)
    step_start = vsketch.Param(-1970)
    step_end = vsketch.Param(1000)
    num_waves = vsketch.Param(1)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=True)
        vsk.scale("mm")

        vsk.rect(0, 0, 297, 210)

        # Draw a sine wave with the given parameters
        sine = lambda x : math.sin(self.frequency * (2 * math.pi * x / self.period)) * self.amplitude

        for j in range(self.num_waves):
            for i in range(self.step_start + j*100, self.step_end, self.interval):
                x1 = i/10
                x2 = i/10 + self.interval/10
                y1 = sine(x1)
                y2 = sine(x2)
                vsk.line(x1, y1, x2, y2)
        

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    VskTestSketch.display()