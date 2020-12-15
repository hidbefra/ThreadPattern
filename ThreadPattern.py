import cv2
import numpy as np
import math
import cmath
import sys
import copy


class ThreadPattern:
    CircleCenter = (0, 0)
    CircleRadius = 0
    Partition = 360
    ImgPath = ""
    lines = []
    sequence = []

    def __init__(self, img_path):
        self.ImgPath = img_path

        img = cv2.imread(self.ImgPath)
        ff = 0.5
        img = cv2.resize(img, None, fx=ff, fy=ff)
        self.gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        shape = self.gray_img.shape

        self.CircleCenter = (int(shape[1] / 2), int(shape[0] / 2))
        self.CircleRadius = min(self.CircleCenter)

    def line_in_kreis(self, a, b):
        xm = self.CircleCenter[0]
        ym = self.CircleCenter[1]
        r = self.CircleRadius
        # Kreismitelpunkt auf (0|0) schiben -> verschieben der geraden
        b = a * xm + b - ym
        if a == 0:
            a = sys.float_info.epsilon  # smallest non negative number
        if b == 0:
            b = sys.float_info.epsilon  # smallest non negative number

        kr = (math.sin(math.atan(1 / a))) / b  # abstand der geraden zu (0|0)
        if abs(kr) < r:
            return True
        else:
            return False

    def round2partition(self, p):
        z = complex(p[0], p[1])
        r, w = cmath.polar(z)

        wt = 2 * math.pi / self.Partition

        pos = int(round(w / wt, 0))
        w = pos * wt

        x = r * math.cos(w)
        y = r * math.sin(w)
        if pos < 0:
            pos = self.Partition + pos
        return x, y, pos

    def intersection_with_circle(self, a, b):
        # (x-xm)^2 + (y-ym)^2 = r^2
        # y = a * x + b

        xm = self.CircleCenter[0]
        ym = self.CircleCenter[1]
        r = self.CircleRadius
        # Kreismitelpunkt auf (0|0) schiben -> verschieben der geraden
        b = a * (xm) + b - ym

        x1 = (math.sqrt((a ** 2 + 1) * r ** 2 - b ** 2) - a * b) / (a ** 2 + 1)
        x2 = -(math.sqrt((a ** 2 + 1) * r ** 2 - b ** 2) + a * b) / (a ** 2 + 1)
        y1 = a * x1 + b
        y2 = a * x2 + b

        (x1, y1, pos1) = self.round2partition((x1, y1))
        (x2, y2, pos2) = self.round2partition((x2, y2))

        if pos1 == pos2:  # das solte nicht pasieren
            print("a={}; b={}; x1={}; y1={}; x2={}; y2={}".format(a, b, x1, y1, x2, y2))

        # um kreismitelpunkt zurückschieben
        x1 += xm
        x2 += xm
        y1 += ym
        y2 += ym

        return (int(round(x1, 0)), int(round(y1, 0))), (int(round(x2, 0)), int(round(y2, 0))), (pos1, pos2)

    def find_lins(self, debug=False):
        gray = self.gray_img

        shape = gray.shape
        control_img = np.zeros(shape, dtype='uint8')
        cv2.circle(control_img, self.CircleCenter, self.CircleRadius, 255)

        edges = cv2.Canny(gray, 50, 150, apertureSize=7)
        sobx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
        soby = cv2.Sobel(gray, cv2.CV_64F, 0, 1)

        self.lines = []
        for x in range(shape[1]):
            if debug:
                numpy_horizontal = np.hstack((edges, 255 - control_img))
                cv2.imshow('numpy_vertical', numpy_horizontal)
                cv2.waitKey(1)

            for y in range(shape[0]):
                if edges[y, x] == 255:

                    mx = sobx[y, x]
                    my = soby[y, x]
                    if my == 0:
                        my = sys.float_info.epsilon  # smallest non negative number
                    a = (-mx) / my
                    if a > max(shape) * 10:  # Steigung der geraden beschränken
                        a = max(shape) * 10
                    if a < (-1) * max(shape) * 10:
                        a = (-1) * max(shape) * 10

                    b = y - (a * x)

                    if self.line_in_kreis(a, b):
                        p1, p2, pos = self.intersection_with_circle(a, b)
                        cv2.line(control_img, p1, p2, 255, 1)

                        # self.lines.append(pos)

                        pos = (max(pos), min(pos))
                        if pos not in self.lines:
                            self.lines.append(pos)

                    edges[y, x] = 0

        return control_img, self.lines

    def poss2coordinate(self, pos):
        r = self.CircleRadius
        (xm, ym) = self.CircleCenter
        wt = 2 * math.pi / self.Partition

        w = pos * wt

        x = r * math.cos(w) + xm
        y = r * math.sin(w) + ym

        return int(round(x, 0)), int(round(y, 0))

    def plot_lines(self):
        shape = self.gray_img.shape
        img = np.zeros(shape, dtype='uint8')
        for pos in self.lines:
            p1 = self.poss2coordinate(pos[0])
            p2 = self.poss2coordinate(pos[1])
            cv2.line(img, p1, p2, 255, 1)
        return img

    def plot_sequence(self, debug=False):
        shape = self.gray_img.shape
        img = np.zeros(shape, dtype='uint8')
        start = self.sequence[0]
        end = self.sequence[1]
        i = 0
        length = 0
        for pos in self.sequence:
            p1 = self.poss2coordinate(start)
            p2 = self.poss2coordinate(end)

            i += 1
            length += round(math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2), 0)

            start = end
            end = pos
            cv2.line(img, p1, p2, 255, 1)

            if debug:
                cv2.imshow('debug plot_sequence', img)
                cv2.waitKey(10)
        length = round((250 / self.CircleRadius * length) / 1000, 0)
        print("{} Linien mit {} m in länge".format(i, length))
        return img

    def find_line_on_pos(self, lines, pos):
        min_length = 20
        solution = []
        for line in lines:
            if line[0] == pos:
                if abs(line[1] - pos) > min_length:
                    solution.append((line, line[1]))
                else:
                    print("zu kurz")
            elif line[1] == pos:
                if abs(line[0] - pos) > min_length:
                    solution.append((line, line[0]))
                else:
                    print("zu kurz")
        return solution

    def move_on_boundary(self, start, end):
        distance = end - start
        direction = int(math.copysign(1, distance))
        return list(range(start + direction, end + direction, direction))

    def sort_lines(self):
        lines_pool = copy.deepcopy(self.lines)
        self.sequence = []

        tmp_line = lines_pool[0]
        self.sequence.append(tmp_line[0])
        on_point = tmp_line[1]
        self.sequence.append(on_point)
        lines_pool.remove(tmp_line)

        while len(lines_pool) > 0:

            options = self.find_line_on_pos(lines_pool, on_point)
            if len(options) == 0:
                # suche den nächsten punkt
                min_dist = 10 ** 10  # Grooser Start wert
                next_point = 0
                for line in lines_pool:
                    dist = abs(line[0] - on_point)
                    if dist < min_dist:
                        min_dist = dist
                        next_point = line[0]
                    dist = abs(line[1] - on_point)
                    if dist < min_dist:
                        min_dist = dist
                        next_point = line[1]

                self.sequence.extend(self.move_on_boundary(on_point, next_point))
                on_point = next_point

            else:
                line_pick = int(len(options) / 2)

                tmp_line = options[line_pick][0]
                on_point = options[line_pick][1]
                self.sequence.append(on_point)
                lines_pool.remove(tmp_line)

        self.sequence.extend(self.move_on_boundary(on_point, on_point + self.Partition + 1))


if __name__ == "__main__":
    input = r"herz-blur3.png"
    c2l = ThreadPattern(input)
    c2l.Partition = 180

    img1, lines = c2l.find_lins(debug=False)
    img2 = c2l.plot_lines()

    c2l.sort_lines()
    img3 = c2l.plot_sequence(debug=False)

    # print(c2l.sequence)

    file = open("ausgabe.txt", "w")
    i = 1
    for point in c2l.sequence:
        tmp = "Punkte[{}]={}".format(i, point)
        file.write(tmp + "\n")
        i += 1
    file.close()

    cv2.imshow('ergebnis', img3)
    cv2.waitKey(0)
