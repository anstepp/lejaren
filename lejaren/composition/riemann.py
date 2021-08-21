class RiemannChord:
    def __init__(self, note_a: int, note_b: int, note_c: int) -> None:
        self.root = note_a
        self.third = note_b
        self.fifth = note_c
        self.major = None
        self.minor = None

        self.proper_voice_leading = [self.root, self.third, self.fifth]
        self.proper_voice_leading.sort()

        test_fifth = (self.fifth - self.root) % 12
        if test_fifth == 7 or test_fifth == -5:
            test_third = (self.third - self.root) % 12
            if test_third == 4 or test_third == -8:

                self.major = True
                self.minor = False
            elif test_third == 3 or test_third == -9:

                self.major = False
                self.minor = True
            else:
                print("test failed - third", test_third)
        else:
            print("test failed - fifth.", test_fifth)

    # parallel
    def P(self):
        if self.major is True:
            new_third = (self.third - 1) % 12
        elif self.minor is True:
            new_third = (self.third + 1) % 12
        return RiemannChord(self.root, new_third, self.fifth)

    # relative
    def R(self):
        if self.major is True:
            new_root = (self.fifth + 2) % 12
            return RiemannChord(new_root, self.root, self.third)
        elif self.minor is True:
            new_fifth = (self.root - 2) % 12
            return RiemannChord(self.third, self.fifth, new_fifth)

    # leading tone
    def L(self):
        if self.major is True:
            new_fifth = (self.root - 1) % 12
            return RiemannChord(self.third, self.fifth, new_fifth)
        elif self.minor is True:
            new_root = (self.fifth + 1) % 12
            return RiemannChord(new_root, self.root, self.third)

    # Slide
    def S(self):
        a = self.L()
        b = a.P()
        c = b.R()
        return c

    # nebenverwandt
    def N(self):
        a = self.R()
        b = a.L()
        c = b.P()
        return c

    # Hexatonic pole
    def H(self):
        a = self.L()
        b = a.P()
        c = b.L()
        return c

    def __str__(self):
        return 'Root: {}, Third: {}, Fifth: {}'.format(
            self.root, self.third, self.fifth
        )
