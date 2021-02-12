#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2020-04-03 20:22:02 using
# version 0.1.0-2 of the sbl2py Snowball-to-Python compiler.

import sys

class _String(object):

    def __init__(self, s):
        self.chars = list(str(s))
        self.cursor = 0
        self.limit = len(s)
        self.direction = 1
        # new stuff, this is to store the sequences of morphemes preceding and following the stem in the word
        self.prefixMorphemes = []
        self.suffixMorphemes = []

    def addPrefix(self, prefix):
        self.prefixMorphemes.append(prefix)
    
    def addSuffix(self, suffix):
        self.suffixMorphemes.append(suffix)

    def __unicode__(self):
        return u''.join(self.chars)

    def __len__(self):
        return len(self.chars)

    def get_range(self, start, stop):
        if self.direction == 1:
            return self.chars[start:stop]
        else:
            n = len(self.chars)
            return self.chars[stop:start]

    def set_range(self, start, stop, chars):
        if self.direction == 1:
            self.chars[start:stop] = chars
        else:
            self.chars[stop:start] = chars
        change = self.direction * (len(chars) - (stop - start))
        if self.direction == 1:
            if self.cursor >= stop:
                self.cursor += change
                self.limit += change
        else:
            if self.cursor > start:
                self.cursor += change
            if self.limit > start:
                self.limit += change
        return True

    def insert(self, chars):
        self.chars[self.cursor:self.cursor] = chars
        if self.direction == 1:
            self.cursor += len(chars)
            self.limit += len(chars)
        return True

    def attach(self, chars):
        self.chars[self.cursor:self.cursor] = chars
        if self.direction == 1:
            self.limit += len(chars)
        else:
            self.cursor += len(chars)
        return True

    def set_chars(self, chars):
        self.chars = chars
        if self.direction == 1:
            self.cursor = 0
            self.limit = len(chars)
        else:
            self.cursor = len(chars)
            self.limit = 0
        return True

    def starts_with(self, chars):
        n = len(chars)
        r = self.get_range(self.cursor, self.limit)[::self.direction][:n]
        if not r == list(chars)[::self.direction]:
            return False
        self.cursor += n * self.direction
        return True

    def hop(self, n):
        if n < 0 or len(self.get_range(self.cursor, self.limit)) < n:
            return False
        self.cursor += n * self.direction
        return True

    def to_mark(self, mark):
        if self.direction == 1:
            if self.cursor > mark or self.limit < mark:
                return False
        else:
            if self.cursor < mark or self.limit > mark:
                return False
        self.cursor = mark
        return True


def stem(s, morphemes=True):
    s = _String(s)
    _Program().r_stem(s)
    if morphemes:
        return s.__unicode__(), s.prefixMorphemes, s.suffixMorphemes[::-1]
    else:
        return s.__unicode__()

_g_q_suffixes = set(u'\u0bbe\u0bcb\u0bc7')
_g_q_prefixes = set(u'\u0b8e')
_g_word_starter = set(u'\u0b95\u0b9a\u0ba4\u0bb5\u0ba8\u0baa\u0bae\u0baf\u0b99\u0b9e')
_g_suttezhuthu = set(u'\u0b85\u0b87\u0b89')
_g_vallinam = set(u'\u0b95\u0b9a\u0b9f\u0ba4\u0baa\u0bb1')
_g_mellinam = set(u'\u0b99\u0b9e\u0ba3\u0ba8\u0bae\u0ba9')
_g_itaiyinam = set(u'\u0baf\u0bb0\u0bb2\u0bb5\u0bb4\u0bb3')
_g_vowel_signs = set(u'\u0bbe\u0bbf\u0bc0\u0bc6\u0bc7\u0bc1\u0bc2\u0bc8')
_g_uyir = set(u'\u0b85\u0b86\u0b87\u0b88\u0b89\u0b8a\u0b8e\u0b8f\u0b90\u0b92\u0b93\u0b94')

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_mark = 0
        self.i_mark2 = 0
        self.b_found_vallinam_doubling = True
        self.b_found_a_match = True
        self.b_found_vetrumai_urupu = True
        self.b_found_wrong_ending = True
        self.b_was_stripped = True
        self.i_length = 0

    def r_strlen(self, s):
        r = True
        self.i_length = 0
        r = True
        if r:
            var1 = s.cursor                              ##
            while True:                        ##        #
                var0 = s.cursor                #         #
                r = s.hop(1)  # next           #         #
                if r:                          #         #
                    self.i_length += 1  ##     #         #
                    r = True            ## +=  # repeat  # do
                if not r:                      #         #
                    s.cursor = var0            #         #
                    break                      #         #
            r = True                           ##        #
            s.cursor = var1                              #
            r = True                                     ##
        return r
    
    def r_has_min_length(self, s):
        r = True
        r = self.r_strlen(s)  # routine call
        if r:
            r = self.i_length > 4  # >
        return r
    
    def r_fix_va_start(self, s):
        r = True
        var12 = s.cursor                                                                     ##
        var9 = s.cursor                                                                ##    #
        var6 = s.cursor                                                          ##    #     #
        var3 = s.cursor                                               ##         #     #     #
        var2 = s.cursor                                        ##     #          #     #     #
        r = s.starts_with(u'\u0bb5\u0bcb')  # character check  #      #          #     #     #
        if not r:                                              # try  #          #     #     #
            r = True                                           #      #          #     #     #
            s.cursor = var2                                    ##     # and      #     #     #
        if r:                                                         #          #     #     #
            s.cursor = var3                                           #          #     #     #
            self.left = s.cursor  ##                                  #          #     #     #
            r = True              ## [                                ##         #     #     #
        if r:                                                                    #     #     #
            r = s.starts_with(u'\u0bb5\u0bcb')  # character check                #     #     #
            if r:                                                                #     #     #
                self.right = s.cursor  ##                                        #     #     #
                r = True               ## ]                                      #     #     #
                if r:                                                            #     #     #
                    r = s.set_range(self.left, self.right, u'\u0b93')  # <-      #     #     #
        if not r:                                                                # or  #     #
            s.cursor = var6                                                      #     #     #
            var5 = s.cursor                                               ##     #     #     #
            var4 = s.cursor                                        ##     #      #     #     #
            r = s.starts_with(u'\u0bb5\u0bca')  # character check  #      #      #     #     #
            if not r:                                              # try  #      #     #     #
                r = True                                           #      #      #     #     #
                s.cursor = var4                                    ##     # and  #     #     #
            if r:                                                         #      #     #     #
                s.cursor = var5                                           #      #     # or  #
                self.left = s.cursor  ##                                  #      #     #     #
                r = True              ## [                                ##     #     #     #
            if r:                                                                #     #     #
                r = s.starts_with(u'\u0bb5\u0bca')  # character check            #     #     #
                if r:                                                            #     #     #
                    self.right = s.cursor  ##                                    #     #     #
                    r = True               ## ]                                  #     #     #
                    if r:                                                        #     #     #
                        r = s.set_range(self.left, self.right, u'\u0b92')  # <-  ##    #     # or
        if not r:                                                                      #     #
            s.cursor = var9                                                            #     #
            var8 = s.cursor                                               ##           #     #
            var7 = s.cursor                                        ##     #            #     #
            r = s.starts_with(u'\u0bb5\u0bc1')  # character check  #      #            #     #
            if not r:                                              # try  #            #     #
                r = True                                           #      #            #     #
                s.cursor = var7                                    ##     # and        #     #
            if r:                                                         #            #     #
                s.cursor = var8                                           #            #     #
                self.left = s.cursor  ##                                  #            #     #
                r = True              ## [                                ##           #     #
            if r:                                                                      #     #
                r = s.starts_with(u'\u0bb5\u0bc1')  # character check                  #     #
                if r:                                                                  #     #
                    self.right = s.cursor  ##                                          #     #
                    r = True               ## ]                                        #     #
                    if r:                                                              #     #
                        r = s.set_range(self.left, self.right, u'\u0b89')  # <-        ##    #
        if not r:                                                                            #
            s.cursor = var12                                                                 #
            var11 = s.cursor                                              ##                 #
            var10 = s.cursor                                       ##     #                  #
            r = s.starts_with(u'\u0bb5\u0bc2')  # character check  #      #                  #
            if not r:                                              # try  #                  #
                r = True                                           #      #                  #
                s.cursor = var10                                   ##     # and              #
            if r:                                                         #                  #
                s.cursor = var11                                          #                  #
                self.left = s.cursor  ##                                  #                  #
                r = True              ## [                                ##                 #
            if r:                                                                            #
                r = s.starts_with(u'\u0bb5\u0bc2')  # character check                        #
                if r:                                                                        #
                    self.right = s.cursor  ##                                                #
                    r = True               ## ]                                              #
                    if r:                                                                    #
                        r = s.set_range(self.left, self.right, u'\u0b8a')  # <-              ##
        return r
    
    def r_fix_endings(self, s):
        r = True
        self.b_found_wrong_ending = True  ##
        r = True                          ## set
        if r:
            while True:                                                  ##
                var14 = s.cursor                                         #
                r = self.b_found_wrong_ending  # boolean variable check  #
                if r:                                                    #
                    var13 = s.cursor                          ##         #
                    r = self.r_fix_ending(s)  # routine call  #          #
                    s.cursor = var13                          # do       # repeat
                    r = True                                  ##         #
                if not r:                                                #
                    s.cursor = var14                                     #
                    break                                                #
            r = True                                                     ##
        return r
    
    def r_remove_question_prefixes(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            r = s.starts_with(u'\u0b8e')  # character check
            if r:
                var23 = s.cursor                                                                                     ##
                var22 = s.cursor                                                                               ##    #
                var21 = s.cursor                                                                         ##    #     #
                var20 = s.cursor                                                                   ##    #     #     #
                var19 = s.cursor                                                             ##    #     #     #     #
                var18 = s.cursor                                                       ##    #     #     #     #     #
                var17 = s.cursor                                                 ##    #     #     #     #     #     #
                var16 = s.cursor                                           ##    #     #     #     #     #     #     #
                var15 = s.cursor                                     ##    #     #     #     #     #     #     #     #
                r = s.starts_with(u'\u0b95')  # character check      #     #     #     #     #     #     #     #     #
                if not r:                                            # or  #     #     #     #     #     #     #     #
                    s.cursor = var15                                 #     # or  #     #     #     #     #     #     #
                    r = s.starts_with(u'\u0b9a')  # character check  ##    #     # or  #     #     #     #     #     #
                if not r:                                                  #     #     # or  #     #     #     #     #
                    s.cursor = var16                                       #     #     #     # or  #     #     #     #
                    r = s.starts_with(u'\u0ba4')  # character check        ##    #     #     #     # or  #     #     #
                if not r:                                                        #     #     #     #     # or  #     #
                    s.cursor = var17                                             #     #     #     #     #     # or  #
                    r = s.starts_with(u'\u0bb5')  # character check              ##    #     #     #     #     #     # or
                if not r:                                                              #     #     #     #     #     #
                    s.cursor = var18                                                   #     #     #     #     #     #
                    r = s.starts_with(u'\u0ba8')  # character check                    ##    #     #     #     #     #
                if not r:                                                                    #     #     #     #     #
                    s.cursor = var19                                                         #     #     #     #     #
                    r = s.starts_with(u'\u0baa')  # character check                          ##    #     #     #     #
                if not r:                                                                          #     #     #     #
                    s.cursor = var20                                                               #     #     #     #
                    r = s.starts_with(u'\u0bae')  # character check                                ##    #     #     #
                if not r:                                                                                #     #     #
                    s.cursor = var21                                                                     #     #     #
                    r = s.starts_with(u'\u0baf')  # character check                                      ##    #     #
                if not r:                                                                                      #     #
                    s.cursor = var22                                                                           #     #
                    r = s.starts_with(u'\u0b99')  # character check                                            ##    #
                if not r:                                                                                            #
                    s.cursor = var23                                                                                 #
                    r = s.starts_with(u'\u0b9e')  # character check                                                  ##
                if r:
                    r = s.starts_with(u'\u0bcd')  # character check
                    if r:
                        self.right = s.cursor  ##
                        r = True               ## ]
                        if r:
                            r = s.set_range(self.left, self.right, u'')  # delete
                            s.addPrefix('question_prefix')
                            if r:
                                var24 = s.cursor                            ##
                                r = self.r_fix_va_start(s)  # routine call  #
                                s.cursor = var24                            # do
                                r = True                                    ##
        return r
    
    def r_fix_ending(self, s):
        r = True
        self.b_found_wrong_ending = False  ##
        r = True                           ## unset
        if r:
            r = self.r_strlen(s)  # routine call
            if r:
                r = self.i_length > 3  # >
                if r:
                    var98 = s.cursor                                                                                                                                                                     ##
                    var99 = len(s) - s.limit                                                                                                                                                             #
                    s.direction *= -1                                                                                                                                                                    #
                    s.cursor, s.limit = s.limit, s.cursor                                                                                                                                                #
                    var97 = len(s) - s.cursor                                                                                                                                                      ##    #
                    var87 = len(s) - s.cursor                                                                                                                                                ##    #     #
                    var86 = len(s) - s.cursor                                                                                                                                          ##    #     #     #
                    var83 = len(s) - s.cursor                                                                                                                                    ##    #     #     #     #
                    var73 = len(s) - s.cursor                                                                                                                              ##    #     #     #     #     #
                    var70 = len(s) - s.cursor                                                                                                                        ##    #     #     #     #     #     #
                    var58 = len(s) - s.cursor                                                                                                                  ##    #     #     #     #     #     #     #
                    var52 = len(s) - s.cursor                                                                                                            ##    #     #     #     #     #     #     #     #
                    var51 = len(s) - s.cursor                                                                                                      ##    #     #     #     #     #     #     #     #     #
                    var40 = len(s) - s.cursor                                                                                                ##    #     #     #     #     #     #     #     #     #     #
                    var38 = len(s) - s.cursor                                                                                          ##    #     #     #     #     #     #     #     #     #     #     #
                    var35 = len(s) - s.cursor                                                                                    ##    #     #     #     #     #     #     #     #     #     #     #     #
                    var34 = len(s) - s.cursor                                                                              ##    #     #     #     #     #     #     #     #     #     #     #     #     #
                    var33 = len(s) - s.cursor                                                                        ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #
                    var32 = len(s) - s.cursor                                                                  ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                    var30 = len(s) - s.cursor                                                            ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                    self.left = s.cursor  ##                                                             #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                    r = True              ## [                                                           #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                    if r:                                                                                #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        var26 = len(s) - s.cursor                                              ##        #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        var25 = len(s) - s.cursor                                        ##    #         #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        r = s.starts_with(u'\u0ba8\u0bcd')  # character check            #     #         #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        if not r:                                                        # or  #         #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            s.cursor = len(s) - var25                                    #     # or      #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            r = s.starts_with(u'\u0ba8\u0bcd\u0ba4')  # character check  ##    #         #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        if not r:                                                              #         #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            s.cursor = len(s) - var26                                          #         #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            r = s.starts_with(u'\u0ba8\u0bcd\u0ba4\u0bcd')  # character check  ##        #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        if r:                                                                            #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            self.right = s.cursor  ##                                                    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            r = True               ## ]                                                  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            if r:                                                                        #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                r = s.set_range(self.left, self.right, u'')  # delete                    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                    if not r:                                                                            #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var30                                                        #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        self.left = s.cursor  ##                                                         # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        r = True              ## [                                                       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        if r:                                                                            #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            r = s.starts_with(u'\u0baf\u0bcd')  # character check                        #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            if r:                                                                        #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                var29 = len(s) - s.cursor                                        ##      #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                var28 = len(s) - s.cursor                                  ##    #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                var27 = len(s) - s.cursor                            ##    #     #       #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                r = s.starts_with(u'\u0bc8')  # character check      #     #     #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                if not r:                                            # or  #     #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var27                        #     # or  # test  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0bbf')  # character check  ##    #     #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                if not r:                                                  #     #       #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var28                              #     #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0bc0')  # character check        ##    #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                s.cursor = len(s) - var29                                        ##      #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                if r:                                                                    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                    self.right = s.cursor  ##                                            #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #
                                    r = True               ## ]                                          #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                    if r:                                                                #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                        r = s.set_range(self.left, self.right, u'')  # delete            ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                    if not r:                                                                                  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var32                                                              #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #
                        self.left = s.cursor  ##                                                               #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        r = True              ## [                                                             #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        if r:                                                                                  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            var31 = len(s) - s.cursor                                              ##          #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            r = s.starts_with(u'\u0b9f\u0bcd\u0baa\u0bcd')  # character check      #           #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            if not r:                                                              # or        #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                s.cursor = len(s) - var31                                          #           #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                r = s.starts_with(u'\u0b9f\u0bcd\u0b95\u0bcd')  # character check  ##          #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            if r:                                                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                self.right = s.cursor  ##                                                      #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                r = True               ## ]                                                    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                if r:                                                                          #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #
                                    r = s.set_range(self.left, self.right, u'\u0bb3\u0bcd')  # <-              ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                    if not r:                                                                                        #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var33                                                                    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        self.left = s.cursor  ##                                                                     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        r = True              ## [                                                                   #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        if r:                                                                                        #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0bcd\u0bb1\u0bcd')  # character check                        #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #
                            if r:                                                                                    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                self.right = s.cursor  ##                                                            #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                r = True               ## ]                                                          #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                if r:                                                                                #     #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                    r = s.set_range(self.left, self.right, u'\u0bb2\u0bcd')  # <-                    ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #
                    if not r:                                                                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var34                                                                          #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        self.left = s.cursor  ##                                                                           #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        r = True              ## [                                                                         #     #     #     #     #     #     #     #     #     #     #     #     #     #
                        if r:                                                                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            r = s.starts_with(u'\u0bb1\u0bcd\u0b95\u0bcd')  # character check                              #     #     #     #     #     #     #     #     #     #     #     #     #     #
                            if r:                                                                                          #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                self.right = s.cursor  ##                                                                  #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                r = True               ## ]                                                                #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                if r:                                                                                      #     #     #     #     #     #     #     #     #     #     #     #     #     #
                                    r = s.set_range(self.left, self.right, u'\u0bb2\u0bcd')  # <-                          ##    #     #     #     #     #     #     #     #     #     #     #     #     #
                    if not r:                                                                                                    #     #     #     #     #     #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var35                                                                                #     #     #     #     #     #     #     #     #     #     #     #     #
                        self.left = s.cursor  ##                                                                                 #     #     #     #     #     #     #     #     #     #     #     #     #
                        r = True              ## [                                                                               #     #     #     #     #     #     #     #     #     #     #     #     #
                        if r:                                                                                                    #     #     #     #     #     #     #     #     #     #     #     #     #
                            r = s.starts_with(u'\u0b9f\u0bcd\u0b9f\u0bcd')  # character check                                    #     #     #     #     #     #     #     #     #     #     #     #     #
                            if r:                                                                                                #     #     #     #     #     #     #     #     #     #     #     #     #
                                self.right = s.cursor  ##                                                                        #     #     #     #     #     #     #     #     #     #     #     #     #
                                r = True               ## ]                                                                      #     #     #     #     #     #     #     #     #     #     #     #     #
                                if r:                                                                                            #     #     #     #     #     #     #     #     #     #     #     #     #
                                    r = s.set_range(self.left, self.right, u'\u0b9f\u0bc1')  # <-                                ##    #     #     #     #     #     #     #     #     #     #     #     #
                    if not r:                                                                                                          #     #     # or  #     #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var38                                                                                      #     #     #     #     #     #     #     #     #     #     #     #
                        r = self.b_found_vetrumai_urupu  # boolean variable check                                                      #     #     #     #     #     #     #     #     #     #     #     #
                        if r:                                                                                                          #     #     #     #     #     #     #     #     #     #     #     #
                            self.left = s.cursor  ##                                                                                   #     #     #     #     #     #     #     #     #     #     #     #
                            r = True              ## [                                                                                 #     #     #     # or  #     #     #     #     #     #     #     #
                            if r:                                                                                                      #     #     #     #     #     #     #     #     #     #     #     #
                                r = s.starts_with(u'\u0ba4\u0bcd\u0ba4\u0bcd')  # character check                                      #     #     #     #     #     #     #     #     #     #     #     #
                                if r:                                                                                                  #     #     #     #     #     #     #     #     #     #     #     #
                                    var37 = len(s) - s.cursor                               ##                                         #     #     #     #     #     #     #     #     #     #     #     #
                                    var36 = len(s) - s.cursor                        ##     #                                          #     #     #     #     #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0bc8')  # character check  #      #                                          #     #     #     #     #     #     #     #     #     #     #     #
                                    if not r:                                        # not  # test                                     #     #     #     #     #     #     #     #     #     #     #     #
                                        s.cursor = len(s) - var36                    #      #                                          #     #     #     #     #     #     #     #     #     #     #     #
                                    r = not r                                        ##     #                                          #     #     #     #     #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var37                               ##                                         #     #     #     #     #     #     #     #     #     #     #     #
                                    if r:                                                                                              #     #     #     #     #     #     #     #     #     #     #     #
                                        self.right = s.cursor  ##                                                                      #     #     #     #     #     #     #     #     #     #     #     #
                                        r = True               ## ]                                                                    #     #     #     #     #     #     #     #     #     #     #     #
                                        if r:                                                                                          #     #     #     #     #     #     #     #     #     #     #     #
                                            r = s.set_range(self.left, self.right, u'\u0bae\u0bcd')  # <-                              #     #     #     #     #     #     #     #     #     #     #     #
                                            if r:                                                                                      #     #     #     #     # or  #     #     #     #     #     #     #
                                                self.right = s.cursor  ##                                                              #     #     #     #     #     #     #     #     #     #     #     #
                                                r = True               ## ]                                                            ##    #     #     #     #     #     #     #     #     #     #     #
                    if not r:                                                                                                                #     #     #     #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var40                                                                                            #     #     #     #     #     #     #     #     #     #     #
                        self.left = s.cursor  ##                                                                                             #     #     #     #     #     #     #     #     #     #     #
                        r = True              ## [                                                                                           #     #     #     #     #     #     #     #     #     #     #
                        if r:                                                                                                                #     #     #     #     #     #     #     #     #     #     #
                            var39 = len(s) - s.cursor                                                    ##                                  #     #     #     #     #     #     #     #     #     #     #
                            r = s.starts_with(u'\u0bc1\u0b95\u0bcd')  # character check                  #                                   #     #     #     #     #     #     #     #     #     #     #
                            if not r:                                                                    # or                                #     #     #     #     #     #     #     #     #     #     #
                                s.cursor = len(s) - var39                                                #                                   #     #     #     #     #     #     #     #     #     #     #
                                r = s.starts_with(u'\u0bc1\u0b95\u0bcd\u0b95\u0bcd')  # character check  ##                                  #     #     #     #     #     #     #     #     #     #     #
                            if r:                                                                                                            #     #     #     #     #     #     #     #     #     #     #
                                self.right = s.cursor  ##                                                                                    #     #     #     #     #     #     #     #     #     #     #
                                r = True               ## ]                                                                                  #     #     #     #     #     #     #     #     #     #     #
                                if r:                                                                                                        #     #     #     #     #     #     #     #     #     #     #
                                    r = s.set_range(self.left, self.right, u'\u0bcd')  # <-                                                  ##    #     #     #     #     #     #     #     #     #     #
                    if not r:                                                                                                                      #     #     #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var51                                                                                                  #     #     #     #     #     #     #     #     #     #
                        self.left = s.cursor  ##                                                                                                   #     #     #     #     #     #     #     #     #     #
                        r = True              ## [                                                                                                 #     #     #     #     #     #     #     #     #     #
                        if r:                                                                                                                      #     #     #     #     #     #     #     #     #     #
                            r = s.starts_with(u'\u0bcd')  # character check                                                                        #     #     #     #     #     #     #     #     #     #
                            if r:                                                                                                                  #     #     #     #     #     #     #     #     #     #
                                var45 = len(s) - s.cursor                                                    ##                                    #     #     #     #     #     #     #     #     #     #
                                var44 = len(s) - s.cursor                                              ##    #                                     #     #     #     #     #     #     #     #     #     #
                                var43 = len(s) - s.cursor                                        ##    #     #                                     #     #     #     #     #     #     #     #     #     #
                                var42 = len(s) - s.cursor                                  ##    #     #     #                                     #     #     #     #     #     #     #     #     #     #
                                var41 = len(s) - s.cursor                            ##    #     #     #     #                                     #     #     #     # or  #     #     #     #     #     #
                                r = s.starts_with(u'\u0b95')  # character check      #     #     #     #     #                                     #     #     #     #     #     #     #     #     #     #
                                if not r:                                            # or  #     #     #     #                                     #     #     #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var41                        #     # or  #     #     #                                     #     #     #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0b9a')  # character check  ##    #     # or  #     #                                     #     #     #     #     #     #     #     #     #     #
                                if not r:                                                  #     #     # or  #                                     #     #     #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var42                              #     #     #     # or                                  #     #     #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0b9f')  # character check        ##    #     #     #                                     #     #     #     #     #     #     #     #     #     #
                                if not r:                                                        #     #     #                                     #     #     #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var43                                    #     #     #                                     #     #     #     #     # or  #     #     #     #     #
                                    r = s.starts_with(u'\u0ba4')  # character check              ##    #     #                                     #     #     #     #     #     #     #     #     #     #
                                if not r:                                                              #     #                                     #     #     #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var44                                          #     #                                     #     #     #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0baa')  # character check                    ##    #                                     #     #     #     #     #     #     #     #     #     #
                                if not r:                                                                    #                                     #     #     #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var45                                                #                                     #     #     #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0bb1')  # character check                          ##                                    #     #     #     #     #     #     #     #     #     #
                                if r:                                                                                                              #     #     #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0bcd')  # character check                                                                #     #     #     #     #     #     #     #     #     #
                                    if r:                                                                                                          #     #     #     #     #     #     #     #     #     #
                                        var50 = len(s) - s.cursor                                                    ##                            #     #     #     #     #     #     #     #     #     #
                                        var49 = len(s) - s.cursor                                              ##    #                             #     #     #     #     #     #     #     #     #     #
                                        var48 = len(s) - s.cursor                                        ##    #     #                             #     #     #     #     #     #     #     #     #     #
                                        var47 = len(s) - s.cursor                                  ##    #     #     #                             #     #     #     #     #     #     #     #     #     #
                                        var46 = len(s) - s.cursor                            ##    #     #     #     #                             #     #     #     #     #     #     #     #     #     #
                                        r = s.starts_with(u'\u0b95')  # character check      #     #     #     #     #                             #     #     #     #     #     #     #     #     #     #
                                        if not r:                                            # or  #     #     #     #                             #     #     #     #     #     #     #     #     #     #
                                            s.cursor = len(s) - var46                        #     # or  #     #     #                             #     #     #     #     #     #     #     #     #     #
                                            r = s.starts_with(u'\u0b9a')  # character check  ##    #     # or  #     #                             #     #     #     #     #     #     #     #     #     #
                                        if not r:                                                  #     #     # or  #                             #     #     #     #     #     #     #     #     #     #
                                            s.cursor = len(s) - var47                              #     #     #     # or                          #     #     #     #     #     #     #     #     #     #
                                            r = s.starts_with(u'\u0b9f')  # character check        ##    #     #     #                             #     #     #     #     #     #     #     #     #     #
                                        if not r:                                                        #     #     #                             #     #     #     #     #     # or  #     #     #     #
                                            s.cursor = len(s) - var48                                    #     #     #                             #     #     #     #     #     #     #     #     #     #
                                            r = s.starts_with(u'\u0ba4')  # character check              ##    #     #                             #     #     #     #     #     #     #     #     #     #
                                        if not r:                                                              #     #                             #     #     #     #     #     #     #     #     #     #
                                            s.cursor = len(s) - var49                                          #     #                             #     #     #     #     #     #     #     #     #     #
                                            r = s.starts_with(u'\u0baa')  # character check                    ##    #                             #     #     #     #     #     #     #     #     #     #
                                        if not r:                                                                    #                             #     #     #     #     #     #     #     #     #     #
                                            s.cursor = len(s) - var50                                                #                             #     #     #     #     #     #     #     #     #     #
                                            r = s.starts_with(u'\u0bb1')  # character check                          ##                            #     #     #     #     #     #     #     #     #     #
                                        if r:                                                                                                      #     #     #     #     #     #     # or  #     #     #
                                            self.right = s.cursor  ##                                                                              #     #     #     #     #     #     #     #     #     #
                                            r = True               ## ]                                                                            #     #     #     #     #     #     #     #     #     #
                                            if r:                                                                                                  #     #     #     #     #     #     #     #     #     #
                                                r = s.set_range(self.left, self.right, u'')  # delete                                              ##    #     #     #     #     #     #     #     #     #
                    if not r:                                                                                                                            #     #     #     #     #     #     # or  #     #
                        s.cursor = len(s) - var52                                                                                                        #     #     #     #     #     #     #     #     #
                        self.left = s.cursor  ##                                                                                                         #     #     #     #     #     #     #     #     #
                        r = True              ## [                                                                                                       #     #     #     #     #     #     #     #     #
                        if r:                                                                                                                            #     #     #     #     #     #     #     #     #
                            r = s.starts_with(u'\u0bc1\u0b95\u0bcd')  # character check                                                                  #     #     #     #     #     #     #     #     #
                            if r:                                                                                                                        #     #     #     #     #     #     #     #     #
                                self.right = s.cursor  ##                                                                                                #     #     #     #     #     #     #     #     #
                                r = True               ## ]                                                                                              #     #     #     #     #     #     #     #     #
                                if r:                                                                                                                    #     #     #     #     #     #     #     #     #
                                    r = s.set_range(self.left, self.right, u'\u0bcd')  # <-                                                              ##    #     #     #     #     #     #     #     #
                    if not r:                                                                                                                                  #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var58                                                                                                              #     #     #     #     #     #     #     #
                        self.left = s.cursor  ##                                                                                                               #     #     #     #     #     #     #     #
                        r = True              ## [                                                                                                             #     #     #     #     #     #     #     #
                        if r:                                                                                                                                  #     #     #     #     #     #     #     #
                            r = s.starts_with(u'\u0bcd')  # character check                                                                                    #     #     #     #     #     #     #     #
                            if r:                                                                                                                              #     #     #     #     #     #     #     #
                                var57 = len(s) - s.cursor                                                    ##                                                #     #     #     #     #     #     #     #
                                var56 = len(s) - s.cursor                                              ##    #                                                 #     #     #     #     #     #     #     #
                                var55 = len(s) - s.cursor                                        ##    #     #                                                 #     #     #     #     #     #     #     #
                                var54 = len(s) - s.cursor                                  ##    #     #     #                                                 #     #     #     #     #     #     #     #
                                var53 = len(s) - s.cursor                            ##    #     #     #     #                                                 #     #     #     #     #     #     #     # backwards
                                r = s.starts_with(u'\u0b95')  # character check      #     #     #     #     #                                                 #     #     #     #     #     #     # or  #
                                if not r:                                            # or  #     #     #     #                                                 #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var53                        #     # or  #     #     #                                                 #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0b9a')  # character check  ##    #     # or  #     #                                                 #     #     #     #     #     #     #     #
                                if not r:                                                  #     #     # or  #                                                 #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var54                              #     #     #     # or                                              #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0b9f')  # character check        ##    #     #     #                                                 #     #     #     #     #     #     #     #
                                if not r:                                                        #     #     #                                                 #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var55                                    #     #     #                                                 #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0ba4')  # character check              ##    #     #                                                 #     #     #     #     #     #     #     #
                                if not r:                                                              #     #                                                 #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var56                                          #     #                                                 #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0baa')  # character check                    ##    #                                                 #     #     #     #     #     #     #     #
                                if not r:                                                                    #                                                 #     #     #     #     #     #     #     #
                                    s.cursor = len(s) - var57                                                #                                                 #     #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0bb1')  # character check                          ##                                                #     #     #     #     #     #     #     #
                                if r:                                                                                                                          #     #     #     #     #     #     #     #
                                    self.right = s.cursor  ##                                                                                                  #     #     #     #     #     #     #     #
                                    r = True               ## ]                                                                                                #     #     #     #     #     #     #     #
                                    if r:                                                                                                                      #     #     #     #     #     #     #     #
                                        r = s.set_range(self.left, self.right, u'')  # delete                                                                  ##    #     #     #     #     #     #     #
                    if not r:                                                                                                                                        #     #     #     #     #     #     #
                        s.cursor = len(s) - var70                                                                                                                    #     #     #     #     #     #     #
                        self.left = s.cursor  ##                                                                                                                     #     #     #     #     #     #     #
                        r = True              ## [                                                                                                                   #     #     #     #     #     #     #
                        if r:                                                                                                                                        #     #     #     #     #     #     #
                            r = s.starts_with(u'\u0bcd')  # character check                                                                                          #     #     #     #     #     #     #
                            if r:                                                                                                                                    #     #     #     #     #     #     #
                                var69 = len(s) - s.cursor                                                              ##                                            #     #     #     #     #     #     #
                                var63 = len(s) - s.cursor                                                    ##        #                                             #     #     #     #     #     #     #
                                var62 = len(s) - s.cursor                                              ##    #         #                                             #     #     #     #     #     #     #
                                var61 = len(s) - s.cursor                                        ##    #     #         #                                             #     #     #     #     #     #     #
                                var60 = len(s) - s.cursor                                  ##    #     #     #         #                                             #     #     #     #     #     #     #
                                var59 = len(s) - s.cursor                            ##    #     #     #     #         #                                             #     #     #     #     #     #     #
                                r = s.starts_with(u'\u0baf')  # character check      #     #     #     #     #         #                                             #     #     #     #     #     #     #
                                if not r:                                            # or  #     #     #     #         #                                             #     #     #     #     #     #     #
                                    s.cursor = len(s) - var59                        #     # or  #     #     #         #                                             #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0bb0')  # character check  ##    #     # or  #     #         #                                             #     #     #     #     #     #     #
                                if not r:                                                  #     #     # or  #         #                                             #     #     #     #     #     #     #
                                    s.cursor = len(s) - var60                              #     #     #     # or      #                                             #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0bb2')  # character check        ##    #     #     #         #                                             #     #     #     #     #     #     #
                                if not r:                                                        #     #     #         #                                             #     #     #     #     #     #     #
                                    s.cursor = len(s) - var61                                    #     #     #         #                                             #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0bb5')  # character check              ##    #     #         #                                             #     #     #     #     #     #     #
                                if not r:                                                              #     #         #                                             #     #     #     #     #     #     #
                                    s.cursor = len(s) - var62                                          #     #         #                                             #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0bb4')  # character check                    ##    #         #                                             #     #     #     #     #     #     #
                                if not r:                                                                    #         #                                             #     #     #     #     #     #     #
                                    s.cursor = len(s) - var63                                                #         #                                             #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0bb3')  # character check                          ##        #                                             #     #     #     #     #     #     #
                                if not r:                                                                              # or                                          #     #     #     #     #     #     #
                                    s.cursor = len(s) - var69                                                          #                                             #     #     #     #     #     #     #
                                    var68 = len(s) - s.cursor                                                    ##    #                                             #     #     #     #     #     #     #
                                    var67 = len(s) - s.cursor                                              ##    #     #                                             #     #     #     #     #     #     #
                                    var66 = len(s) - s.cursor                                        ##    #     #     #                                             #     #     #     #     #     #     #
                                    var65 = len(s) - s.cursor                                  ##    #     #     #     #                                             #     #     #     #     #     #     #
                                    var64 = len(s) - s.cursor                            ##    #     #     #     #     #                                             #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0b99')  # character check      #     #     #     #     #     #                                             #     #     #     #     #     #     #
                                    if not r:                                            # or  #     #     #     #     #                                             #     #     #     #     #     #     #
                                        s.cursor = len(s) - var64                        #     # or  #     #     #     #                                             #     #     #     #     #     #     #
                                        r = s.starts_with(u'\u0b9e')  # character check  ##    #     # or  #     #     #                                             #     #     #     #     #     #     #
                                    if not r:                                                  #     #     # or  #     #                                             #     #     #     #     #     #     #
                                        s.cursor = len(s) - var65                              #     #     #     # or  #                                             #     #     #     #     #     #     #
                                        r = s.starts_with(u'\u0ba3')  # character check        ##    #     #     #     #                                             #     #     #     #     #     #     #
                                    if not r:                                                        #     #     #     #                                             #     #     #     #     #     #     #
                                        s.cursor = len(s) - var66                                    #     #     #     #                                             #     #     #     #     #     #     #
                                        r = s.starts_with(u'\u0ba8')  # character check              ##    #     #     #                                             #     #     #     #     #     #     #
                                    if not r:                                                              #     #     #                                             #     #     #     #     #     #     #
                                        s.cursor = len(s) - var67                                          #     #     #                                             #     #     #     #     #     #     #
                                        r = s.starts_with(u'\u0bae')  # character check                    ##    #     #                                             #     #     #     #     #     #     #
                                    if not r:                                                                    #     #                                             #     #     #     #     #     #     #
                                        s.cursor = len(s) - var68                                                #     #                                             #     #     #     #     #     #     #
                                        r = s.starts_with(u'\u0ba9')  # character check                          ##    ##                                            #     #     #     #     #     #     #
                                if r:                                                                                                                                #     #     #     #     #     #     #
                                    r = s.starts_with(u'\u0bcd')  # character check                                                                                  #     #     #     #     #     #     #
                                    if r:                                                                                                                            #     #     #     #     #     #     #
                                        self.right = s.cursor  ##                                                                                                    #     #     #     #     #     #     #
                                        r = True               ## ]                                                                                                  #     #     #     #     #     #     #
                                        if r:                                                                                                                        #     #     #     #     #     #     #
                                            r = s.set_range(self.left, self.right, u'\u0bcd')  # <-                                                                  ##    #     #     #     #     #     #
                    if not r:                                                                                                                                              #     #     #     #     #     #
                        s.cursor = len(s) - var73                                                                                                                          #     #     #     #     #     #
                        self.left = s.cursor  ##                                                                                                                           #     #     #     #     #     #
                        r = True              ## [                                                                                                                         #     #     #     #     #     #
                        if r:                                                                                                                                              #     #     #     #     #     #
                            var72 = len(s) - s.cursor                                  ##                                                                                  #     #     #     #     #     #
                            var71 = len(s) - s.cursor                            ##    #                                                                                   #     #     #     #     #     #
                            r = s.starts_with(u'\u0bb5')  # character check      #     #                                                                                   #     #     #     #     #     #
                            if not r:                                            # or  #                                                                                   #     #     #     #     #     #
                                s.cursor = len(s) - var71                        #     # or                                                                                #     #     #     #     #     #
                                r = s.starts_with(u'\u0baf')  # character check  ##    #                                                                                   #     #     #     #     #     #
                            if not r:                                                  #                                                                                   #     #     #     #     #     #
                                s.cursor = len(s) - var72                              #                                                                                   #     #     #     #     #     #
                                r = s.starts_with(u'\u0bb5\u0bcd')  # character check  ##                                                                                  #     #     #     #     #     #
                            if r:                                                                                                                                          #     #     #     #     #     #
                                self.right = s.cursor  ##                                                                                                                  #     #     #     #     #     #
                                r = True               ## ]                                                                                                                #     #     #     #     #     #
                                if r:                                                                                                                                      #     #     #     #     #     #
                                    r = s.set_range(self.left, self.right, u'')  # delete                                                                                  ##    #     #     #     #     #
                    if not r:                                                                                                                                                    #     #     #     #     #
                        s.cursor = len(s) - var83                                                                                                                                #     #     #     #     #
                        self.left = s.cursor  ##                                                                                                                                 #     #     #     #     #
                        r = True              ## [                                                                                                                               #     #     #     #     #
                        if r:                                                                                                                                                    #     #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0bc1')  # character check                                                                                                #     #     #     #     #
                            if r:                                                                                                                                                #     #     #     #     #
                                var82 = len(s) - s.cursor                                                                             ##                                         #     #     #     #     #
                                var81 = len(s) - s.cursor                                                                      ##     #                                          #     #     #     #     #
                                var80 = len(s) - s.cursor                                                                ##    #      #                                          #     #     #     #     #
                                var79 = len(s) - s.cursor                                                          ##    #     #      #                                          #     #     #     #     #
                                var78 = len(s) - s.cursor                                                    ##    #     #     #      #                                          #     #     #     #     #
                                var77 = len(s) - s.cursor                                              ##    #     #     #     #      #                                          #     #     #     #     #
                                var76 = len(s) - s.cursor                                        ##    #     #     #     #     #      #                                          #     #     #     #     #
                                var75 = len(s) - s.cursor                                  ##    #     #     #     #     #     #      #                                          #     #     #     #     #
                                var74 = len(s) - s.cursor                            ##    #     #     #     #     #     #     #      #                                          #     #     #     #     #
                                r = s.starts_with(u'\u0bbe')  # character check      #     #     #     #     #     #     #     #      #                                          #     #     #     #     #
                                if not r:                                            # or  #     #     #     #     #     #     #      #                                          #     #     #     #     #
                                    s.cursor = len(s) - var74                        #     # or  #     #     #     #     #     #      #                                          #     #     #     #     #
                                    r = s.starts_with(u'\u0bbf')  # character check  ##    #     # or  #     #     #     #     #      #                                          #     #     #     #     #
                                if not r:                                                  #     #     # or  #     #     #     #      #                                          #     #     #     #     #
                                    s.cursor = len(s) - var75                              #     #     #     # or  #     #     #      #                                          #     #     #     #     #
                                    r = s.starts_with(u'\u0bc0')  # character check        ##    #     #     #     # or  #     #      #                                          #     #     #     #     #
                                if not r:                                                        #     #     #     #     # or  #      #                                          #     #     #     #     #
                                    s.cursor = len(s) - var76                                    #     #     #     #     #     # not  # test                                     #     #     #     #     #
                                    r = s.starts_with(u'\u0bc6')  # character check              ##    #     #     #     #     #      #                                          #     #     #     #     #
                                if not r:                                                              #     #     #     #     #      #                                          #     #     #     #     #
                                    s.cursor = len(s) - var77                                          #     #     #     #     #      #                                          #     #     #     #     #
                                    r = s.starts_with(u'\u0bc7')  # character check                    ##    #     #     #     #      #                                          #     #     #     #     #
                                if not r:                                                                    #     #     #     #      #                                          #     #     #     #     #
                                    s.cursor = len(s) - var78                                                #     #     #     #      #                                          #     #     #     #     #
                                    r = s.starts_with(u'\u0bc1')  # character check                          ##    #     #     #      #                                          #     #     #     #     #
                                if not r:                                                                          #     #     #      #                                          #     #     #     #     #
                                    s.cursor = len(s) - var79                                                      #     #     #      #                                          #     #     #     #     #
                                    r = s.starts_with(u'\u0bc2')  # character check                                ##    #     #      #                                          #     #     #     #     #
                                if not r:                                                                                #     #      #                                          #     #     #     #     #
                                    s.cursor = len(s) - var80                                                            #     #      #                                          #     #     #     #     #
                                    r = s.starts_with(u'\u0bc8')  # character check                                      ##    #      #                                          #     #     #     #     #
                                if not r:                                                                                      #      #                                          #     #     #     #     #
                                    s.cursor = len(s) - var81                                                                  #      #                                          #     #     #     #     #
                                r = not r                                                                                      ##     #                                          #     #     #     #     #
                                s.cursor = len(s) - var82                                                                             ##                                         #     #     #     #     #
                                if r:                                                                                                                                            #     #     #     #     #
                                    self.right = s.cursor  ##                                                                                                                    #     #     #     #     #
                                    r = True               ## ]                                                                                                                  #     #     #     #     #
                                    if r:                                                                                                                                        #     #     #     #     #
                                        r = s.set_range(self.left, self.right, u'')  # delete                                                                                    ##    #     #     #     #
                    if not r:                                                                                                                                                          #     #     #     #
                        s.cursor = len(s) - var86                                                                                                                                      #     #     #     #
                        self.left = s.cursor  ##                                                                                                                                       #     #     #     #
                        r = True              ## [                                                                                                                                     #     #     #     #
                        if r:                                                                                                                                                          #     #     #     #
                            r = s.starts_with(u'\u0b99\u0bcd')  # character check                                                                                                      #     #     #     #
                            if r:                                                                                                                                                      #     #     #     #
                                var85 = len(s) - s.cursor                               ##                                                                                             #     #     #     #
                                var84 = len(s) - s.cursor                        ##     #                                                                                              #     #     #     #
                                r = s.starts_with(u'\u0bc8')  # character check  #      #                                                                                              #     #     #     #
                                if not r:                                        # not  # test                                                                                         #     #     #     #
                                    s.cursor = len(s) - var84                    #      #                                                                                              #     #     #     #
                                r = not r                                        ##     #                                                                                              #     #     #     #
                                s.cursor = len(s) - var85                               ##                                                                                             #     #     #     #
                                if r:                                                                                                                                                  #     #     #     #
                                    self.right = s.cursor  ##                                                                                                                          #     #     #     #
                                    r = True               ## ]                                                                                                                        #     #     #     #
                                    if r:                                                                                                                                              #     #     #     #
                                        r = s.set_range(self.left, self.right, u'\u0bae\u0bcd')  # <-                                                                                  ##    #     #     #
                    if not r:                                                                                                                                                                #     #     #
                        s.cursor = len(s) - var87                                                                                                                                            #     #     #
                        self.left = s.cursor  ##                                                                                                                                             #     #     #
                        r = True              ## [                                                                                                                                           #     #     #
                        if r:                                                                                                                                                                #     #     #
                            r = s.starts_with(u'\u0b99\u0bcd')  # character check                                                                                                            #     #     #
                            if r:                                                                                                                                                            #     #     #
                                self.right = s.cursor  ##                                                                                                                                    #     #     #
                                r = True               ## ]                                                                                                                                  #     #     #
                                if r:                                                                                                                                                        #     #     #
                                    r = s.set_range(self.left, self.right, u'')  # delete                                                                                                    ##    #     #
                    if not r:                                                                                                                                                                      #     #
                        s.cursor = len(s) - var97                                                                                                                                                  #     #
                        self.left = s.cursor  ##                                                                                                                                                   #     #
                        r = True              ## [                                                                                                                                                 #     #
                        if r:                                                                                                                                                                      #     #
                            r = s.starts_with(u'\u0bcd')  # character check                                                                                                                        #     #
                            if r:                                                                                                                                                                  #     #
                                var96 = len(s) - s.cursor                                                                            ##                                                            #     #
                                var95 = len(s) - s.cursor                                                                      ##    #                                                             #     #
                                var94 = len(s) - s.cursor                                                                ##    #     #                                                             #     #
                                var93 = len(s) - s.cursor                                                          ##    #     #     #                                                             #     #
                                var92 = len(s) - s.cursor                                                    ##    #     #     #     #                                                             #     #
                                var91 = len(s) - s.cursor                                              ##    #     #     #     #     #                                                             #     #
                                var90 = len(s) - s.cursor                                        ##    #     #     #     #     #     #                                                             #     #
                                var89 = len(s) - s.cursor                                  ##    #     #     #     #     #     #     #                                                             #     #
                                var88 = len(s) - s.cursor                            ##    #     #     #     #     #     #     #     #                                                             #     #
                                r = s.starts_with(u'\u0bbe')  # character check      #     #     #     #     #     #     #     #     #                                                             #     #
                                if not r:                                            # or  #     #     #     #     #     #     #     #                                                             #     #
                                    s.cursor = len(s) - var88                        #     # or  #     #     #     #     #     #     #                                                             #     #
                                    r = s.starts_with(u'\u0bbf')  # character check  ##    #     # or  #     #     #     #     #     #                                                             #     #
                                if not r:                                                  #     #     # or  #     #     #     #     #                                                             #     #
                                    s.cursor = len(s) - var89                              #     #     #     # or  #     #     #     #                                                             #     #
                                    r = s.starts_with(u'\u0bc0')  # character check        ##    #     #     #     # or  #     #     #                                                             #     #
                                if not r:                                                        #     #     #     #     # or  #     #                                                             #     #
                                    s.cursor = len(s) - var90                                    #     #     #     #     #     # or  # test                                                        #     #
                                    r = s.starts_with(u'\u0bc6')  # character check              ##    #     #     #     #     #     #                                                             #     #
                                if not r:                                                              #     #     #     #     #     #                                                             #     #
                                    s.cursor = len(s) - var91                                          #     #     #     #     #     #                                                             #     #
                                    r = s.starts_with(u'\u0bc7')  # character check                    ##    #     #     #     #     #                                                             #     #
                                if not r:                                                                    #     #     #     #     #                                                             #     #
                                    s.cursor = len(s) - var92                                                #     #     #     #     #                                                             #     #
                                    r = s.starts_with(u'\u0bc1')  # character check                          ##    #     #     #     #                                                             #     #
                                if not r:                                                                          #     #     #     #                                                             #     #
                                    s.cursor = len(s) - var93                                                      #     #     #     #                                                             #     #
                                    r = s.starts_with(u'\u0bc2')  # character check                                ##    #     #     #                                                             #     #
                                if not r:                                                                                #     #     #                                                             #     #
                                    s.cursor = len(s) - var94                                                            #     #     #                                                             #     #
                                    r = s.starts_with(u'\u0bc8')  # character check                                      ##    #     #                                                             #     #
                                if not r:                                                                                      #     #                                                             #     #
                                    s.cursor = len(s) - var95                                                                  #     #                                                             #     #
                                    r = s.starts_with(u'\u0bcd')  # character check                                            ##    #                                                             #     #
                                s.cursor = len(s) - var96                                                                            ##                                                            #     #
                                if r:                                                                                                                                                              #     #
                                    self.right = s.cursor  ##                                                                                                                                      #     #
                                    r = True               ## ]                                                                                                                                    #     #
                                    if r:                                                                                                                                                          #     #
                                        r = s.set_range(self.left, self.right, u'')  # delete                                                                                                      ##    #
                    s.direction *= -1                                                                                                                                                                    #
                    s.cursor = var98                                                                                                                                                                     #
                    s.limit = len(s) - var99                                                                                                                                                             ##
                    if r:
                        self.b_found_wrong_ending = True  ##
                        r = True                          ## set
        return r
    
    def r_remove_pronoun_prefixes(self, s):
        r = True
        self.b_found_a_match = False  ##
        r = True                      ## unset
        if r:
            self.left = s.cursor  ##
            r = True              ## [
            if r:
                var101 = s.cursor                                          ##
                var100 = s.cursor                                    ##    #
                r = s.starts_with(u'\u0b85')  # character check      #     #
                pronounPrefix = "pronoun_prefix_a"
                if not r:                                            # or  #
                    s.cursor = var100                                #     # or
                    r = s.starts_with(u'\u0b87')  # character check  ##    #
                    pronounPrefix = "pronoun_prefix_i"
                if not r:                                                  #
                    s.cursor = var101                                      #
                    r = s.starts_with(u'\u0b89')  # character check        ##
                    pronounPrefix = "pronoun_prefix_u"
                if r:
                    var110 = s.cursor                                                                                    ##
                    var109 = s.cursor                                                                              ##    #
                    var108 = s.cursor                                                                        ##    #     #
                    var107 = s.cursor                                                                  ##    #     #     #
                    var106 = s.cursor                                                            ##    #     #     #     #
                    var105 = s.cursor                                                      ##    #     #     #     #     #
                    var104 = s.cursor                                                ##    #     #     #     #     #     #
                    var103 = s.cursor                                          ##    #     #     #     #     #     #     #
                    var102 = s.cursor                                    ##    #     #     #     #     #     #     #     #
                    r = s.starts_with(u'\u0b95')  # character check      #     #     #     #     #     #     #     #     #
                    if not r:                                            # or  #     #     #     #     #     #     #     #
                        s.cursor = var102                                #     # or  #     #     #     #     #     #     #
                        r = s.starts_with(u'\u0b9a')  # character check  ##    #     # or  #     #     #     #     #     #
                    if not r:                                                  #     #     # or  #     #     #     #     #
                        s.cursor = var103                                      #     #     #     # or  #     #     #     #
                        r = s.starts_with(u'\u0ba4')  # character check        ##    #     #     #     # or  #     #     #
                    if not r:                                                        #     #     #     #     # or  #     #
                        s.cursor = var104                                            #     #     #     #     #     # or  #
                        r = s.starts_with(u'\u0bb5')  # character check              ##    #     #     #     #     #     # or
                    if not r:                                                              #     #     #     #     #     #
                        s.cursor = var105                                                  #     #     #     #     #     #
                        r = s.starts_with(u'\u0ba8')  # character check                    ##    #     #     #     #     #
                    if not r:                                                                    #     #     #     #     #
                        s.cursor = var106                                                        #     #     #     #     #
                        r = s.starts_with(u'\u0baa')  # character check                          ##    #     #     #     #
                    if not r:                                                                          #     #     #     #
                        s.cursor = var107                                                              #     #     #     #
                        r = s.starts_with(u'\u0bae')  # character check                                ##    #     #     #
                    if not r:                                                                                #     #     #
                        s.cursor = var108                                                                    #     #     #
                        r = s.starts_with(u'\u0baf')  # character check                                      ##    #     #
                    if not r:                                                                                      #     #
                        s.cursor = var109                                                                          #     #
                        r = s.starts_with(u'\u0b99')  # character check                                            ##    #
                    if not r:                                                                                            #
                        s.cursor = var110                                                                                #
                        r = s.starts_with(u'\u0b9e')  # character check                                                  ##
                    if r:
                        r = s.starts_with(u'\u0bcd')  # character check
                        if r:
                            self.right = s.cursor  ##
                            r = True               ## ]
                            if r:
                                r = s.set_range(self.left, self.right, u'')  # delete
                                s.addPrefix(pronounPrefix)
                                if r:
                                    self.b_found_a_match = True  ##
                                    r = True                     ## set
                                    if r:
                                        var111 = s.cursor                           ##
                                        r = self.r_fix_va_start(s)  # routine call  #
                                        s.cursor = var111                           # do
                                        r = True                                    ##
        return r
    
    def r_remove_plural_suffix(self, s):
        r = True
        self.b_found_a_match = False  ##
        r = True                      ## unset
        if r:
            var122 = s.cursor                                                                                                           ##
            var123 = len(s) - s.limit                                                                                                   #
            s.direction *= -1                                                                                                           #
            s.cursor, s.limit = s.limit, s.cursor                                                                                       #
            var121 = len(s) - s.cursor                                                                                            ##    #
            var120 = len(s) - s.cursor                                                                                      ##    #     #
            var119 = len(s) - s.cursor                                                                                ##    #     #     #
            self.left = s.cursor  ##                                                                                  #     #     #     #
            r = True              ## [                                                                                #     #     #     #
            if r:                                                                                                     #     #     #     #
                r = s.starts_with(u'\u0bc1\u0b99\u0bcd\u0b95\u0bb3\u0bcd')  # character check                         #     #     #     #
                if r:                                                                                                 #     #     #     #
                    var118 = len(s) - s.cursor                                                                ##      #     #     #     #
                    var117 = len(s) - s.cursor                                                         ##     #       #     #     #     #
                    var116 = len(s) - s.cursor                                                   ##    #      #       #     #     #     #
                    var115 = len(s) - s.cursor                                             ##    #     #      #       #     #     #     #
                    var114 = len(s) - s.cursor                                       ##    #     #     #      #       #     #     #     #
                    var113 = len(s) - s.cursor                                 ##    #     #     #     #      #       #     #     #     #
                    var112 = len(s) - s.cursor                           ##    #     #     #     #     #      #       #     #     #     #
                    r = s.starts_with(u'\u0b95')  # character check      #     #     #     #     #     #      #       #     #     #     #
                    if not r:                                            # or  #     #     #     #     #      #       #     #     #     #
                        s.cursor = len(s) - var112                       #     # or  #     #     #     #      #       #     #     #     #
                        r = s.starts_with(u'\u0b9a')  # character check  ##    #     # or  #     #     #      #       #     #     #     #
                    if not r:                                                  #     #     # or  #     #      #       #     #     #     #
                        s.cursor = len(s) - var113                             #     #     #     # or  #      #       #     #     #     #
                        r = s.starts_with(u'\u0b9f')  # character check        ##    #     #     #     # not  # test  #     #     #     #
                    if not r:                                                        #     #     #     #      #       #     #     #     #
                        s.cursor = len(s) - var114                                   #     #     #     #      #       #     #     #     #
                        r = s.starts_with(u'\u0ba4')  # character check              ##    #     #     #      #       #     #     #     #
                    if not r:                                                              #     #     #      #       #     #     #     #
                        s.cursor = len(s) - var115                                         #     #     #      #       # or  #     #     #
                        r = s.starts_with(u'\u0baa')  # character check                    ##    #     #      #       #     #     #     #
                    if not r:                                                                    #     #      #       #     #     #     #
                        s.cursor = len(s) - var116                                               #     #      #       #     #     #     #
                        r = s.starts_with(u'\u0bb1')  # character check                          ##    #      #       #     #     #     #
                    if not r:                                                                          #      #       #     # or  #     #
                        s.cursor = len(s) - var117                                                     #      #       #     #     #     #
                    r = not r                                                                          ##     #       #     #     #     #
                    s.cursor = len(s) - var118                                                                ##      #     #     #     #
                    if r:                                                                                             #     #     #     #
                        self.right = s.cursor  ##                                                                     #     #     # or  #
                        r = True               ## ]                                                                   #     #     #     # backwards
                        if r:                                                                                         #     #     #     #
                            r = s.set_range(self.left, self.right, u'\u0bcd')  # <-                                   #     #     #     #
            if not r:                                                                                                 #     #     #     #
                s.cursor = len(s) - var119                                                                            #     #     #     #
                self.left = s.cursor  ##                                                                              #     #     #     #
                r = True              ## [                                                                            #     #     #     #
                if r:                                                                                                 #     #     #     #
                    r = s.starts_with(u'\u0bb1\u0bcd\u0b95\u0bb3\u0bcd')  # character check                           #     #     #     #
                    if r:                                                                                             #     #     #     #
                        self.right = s.cursor  ##                                                                     #     #     #     #
                        r = True               ## ]                                                                   #     #     #     #
                        if r:                                                                                         #     #     #     #
                            r = s.set_range(self.left, self.right, u'\u0bb2\u0bcd')  # <-                             ##    #     #     #
            if not r:                                                                                                       #     #     #
                s.cursor = len(s) - var120                                                                                  #     #     #
                self.left = s.cursor  ##                                                                                    #     #     #
                r = True              ## [                                                                                  #     #     #
                if r:                                                                                                       #     #     #
                    r = s.starts_with(u'\u0b9f\u0bcd\u0b95\u0bb3\u0bcd')  # character check                                 #     #     #
                    if r:                                                                                                   #     #     #
                        self.right = s.cursor  ##                                                                           #     #     #
                        r = True               ## ]                                                                         #     #     #
                        if r:                                                                                               #     #     #
                            r = s.set_range(self.left, self.right, u'\u0bb3\u0bcd')  # <-                                   ##    #     #
            if not r:                                                                                                             #     #
                s.cursor = len(s) - var121                                                                                        #     #
                self.left = s.cursor  ##                                                                                          #     #
                r = True              ## [                                                                                        #     #
                if r:                                                                                                             #     #
                    r = s.starts_with(u'\u0b95\u0bb3\u0bcd')  # character check                                                   #     #
                    if r:                                                                                                         #     #
                        self.right = s.cursor  ##                                                                                 #     #
                        r = True               ## ]                                                                               #     #
                        if r:                                                                                                     #     #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                 ##    #
                            s.addSuffix('plural_suffix')
            if r:                                                                                                                       #
                self.b_found_a_match = True  ##                                                                                         #
                r = True                     ## set                                                                                     #
            s.direction *= -1                                                                                                           #
            s.cursor = var122                                                                                                           #
            s.limit = len(s) - var123                                                                                                   ##
            if r:
                var124 = s.cursor                          ##
                r = self.r_fix_endings(s)  # routine call  #
                s.cursor = var124                          # do
                r = True                                   ##
        return r
    
    def r_remove_question_suffixes(self, s):
        r = True
        r = self.r_has_min_length(s)  # routine call
        if r:
            self.b_found_a_match = False  ##
            r = True                      ## unset
            if r:
                var128 = s.cursor                                                          ##
                var129 = len(s) - s.limit                                                  #
                s.direction *= -1                                                          #
                s.cursor, s.limit = s.limit, s.cursor                                      #
                var127 = len(s) - s.cursor                                           ##    #
                self.left = s.cursor  ##                                             #     #
                r = True              ## [                                           #     #
                if r:                                                                #     #
                    var126 = len(s) - s.cursor                                 ##    #     #
                    var125 = len(s) - s.cursor                           ##    #     #     #
                    r = s.starts_with(u'\u0bcb')  # character check      #     #     #     #
                    questionSuffix = "question_suffix_oo"
                    if not r:                                            # or  #     #     #
                        s.cursor = len(s) - var125                       #     # or  #     #
                        r = s.starts_with(u'\u0bc7')  # character check  ##    #     #     #
                        questionSuffix = "question_suffix_ee"
                    if not r:                                                  #     #     #
                        s.cursor = len(s) - var126                             #     # do  # backwards
                        r = s.starts_with(u'\u0bbe')  # character check        ##    #     #
                        questionSuffix = "question_suffix_aa"
                    if r:                                                            #     #
                        self.right = s.cursor  ##                                    #     #
                        r = True               ## ]                                  #     #
                        if r:                                                        #     #
                            r = s.set_range(self.left, self.right, u'\u0bcd')  # <-  #     #
                            s.addSuffix(questionSuffix)
                            if r:                                                    #     #
                                self.b_found_a_match = True  ##                      #     #
                                r = True                     ## set                  #     #
                s.cursor = len(s) - var127                                           #     #
                r = True                                                             ##    #
                s.direction *= -1                                                          #
                s.cursor = var128                                                          #
                s.limit = len(s) - var129                                                  ##
                if r:
                    var130 = s.cursor                          ##
                    r = self.r_fix_endings(s)  # routine call  #
                    s.cursor = var130                          # do
                    r = True                                   ##
        return r
    
    def r_remove_command_suffixes(self, s):
        r = True
        r = self.r_has_min_length(s)  # routine call
        if r:
            self.b_found_a_match = False  ##
            r = True                      ## unset
            if r:
                var132 = s.cursor                                                    ##
                var133 = len(s) - s.limit                                            #
                s.direction *= -1                                                    #
                s.cursor, s.limit = s.limit, s.cursor                                #
                self.left = s.cursor  ##                                             #
                r = True              ## [                                           #
                if r:                                                                #
                    var131 = len(s) - s.cursor                                 ##    #
                    r = s.starts_with(u'\u0baa\u0bbf')  # character check      #     #
                    commandSuffix = 'command_suffix_pi'
                    if not r:                                                  # or  #
                        s.cursor = len(s) - var131                             #     #
                        r = s.starts_with(u'\u0bb5\u0bbf')  # character check  ##    # backwards
                        commandSuffix = 'command_suffix_vi'
                    if r:                                                            #
                        self.right = s.cursor  ##                                    #
                        r = True               ## ]                                  #
                        if r:                                                        #
                            r = s.set_range(self.left, self.right, u'')  # delete    #
                            s.addSuffix(commandSuffix)
                            if r:                                                    #
                                self.b_found_a_match = True  ##                      #
                                r = True                     ## set                  #
                s.direction *= -1                                                    #
                s.cursor = var132                                                    #
                s.limit = len(s) - var133                                            ##
        return r
    
    def r_remove_um(self, s):
        r = True
        self.b_found_a_match = False  ##
        r = True                      ## unset
        if r:
            r = self.r_has_min_length(s)  # routine call
            if r:
                var134 = s.cursor                                                    ##
                var135 = len(s) - s.limit                                            #
                s.direction *= -1                                                    #
                s.cursor, s.limit = s.limit, s.cursor                                #
                self.left = s.cursor  ##                                             #
                r = True              ## [                                           #
                if r:                                                                #
                    r = s.starts_with(u'\u0bc1\u0bae\u0bcd')  # character check      #
                    if r:                                                            #
                        self.right = s.cursor  ##                                    # backwards
                        r = True               ## ]                                  #
                        if r:                                                        #
                            r = s.set_range(self.left, self.right, u'\u0bcd')  # <-  #
                            s.addSuffix('suffix_um')
                            if r:                                                    #
                                self.b_found_a_match = True  ##                      #
                                r = True                     ## set                  #
                s.direction *= -1                                                    #
                s.cursor = var134                                                    #
                s.limit = len(s) - var135                                            ##
                if r:
                    var136 = s.cursor                         ##
                    r = self.r_fix_ending(s)  # routine call  #
                    s.cursor = var136                         # do
                    r = True                                  ##
        return r
    
    def r_remove_common_word_endings(self, s):
        r = True
        self.b_found_a_match = False  ##
        r = True                      ## unset
        if r:
            r = self.r_has_min_length(s)  # routine call
            if r:
                var175 = s.cursor                                                                                                                                                            ##
                var176 = len(s) - s.limit                                                                                                                                                    #
                s.direction *= -1                                                                                                                                                            #
                s.cursor, s.limit = s.limit, s.cursor                                                                                                                                        #
                var174 = len(s) - s.cursor                                                                                                                                             ##    #
                var159 = len(s) - s.cursor                                                                                                                                     ##      #     #
                self.left = s.cursor  ##                                                                                                                                       #       #     #
                r = True              ## [                                                                                                                                     #       #     #
                if r:                                                                                                                                                          #       #     #
                    var158 = len(s) - s.cursor                                                                                                                           ##    #       #     #
                    var157 = len(s) - s.cursor                                                                                                                     ##    #     #       #     #
                    var156 = len(s) - s.cursor                                                                                                               ##    #     #     #       #     #
                    var146 = len(s) - s.cursor                                                                                                         ##    #     #     #     #       #     #
                    var145 = len(s) - s.cursor                                                                                                   ##    #     #     #     #     #       #     #
                    var144 = len(s) - s.cursor                                                                                             ##    #     #     #     #     #     #       #     #
                    var143 = len(s) - s.cursor                                                                                       ##    #     #     #     #     #     #     #       #     #
                    var142 = len(s) - s.cursor                                                                                 ##    #     #     #     #     #     #     #     #       #     #
                    var141 = len(s) - s.cursor                                                                           ##    #     #     #     #     #     #     #     #     #       #     #
                    var140 = len(s) - s.cursor                                                                     ##    #     #     #     #     #     #     #     #     #     #       #     #
                    var139 = len(s) - s.cursor                                                               ##    #     #     #     #     #     #     #     #     #     #     #       #     #
                    var138 = len(s) - s.cursor                                                         ##    #     #     #     #     #     #     #     #     #     #     #     #       #     #
                    var137 = len(s) - s.cursor                                                   ##    #     #     #     #     #     #     #     #     #     #     #     #     #       #     #
                    r = s.starts_with(u'\u0bc1\u0b9f\u0ba9\u0bcd')  # character check            #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #
                    wordEnding = "common_suffix_udan"
                    if not r:                                                                    # or  #     #     #     #     #     #     #     #     #     #     #     #     #       #     #
                        s.cursor = len(s) - var137                                               #     # or  #     #     #     #     #     #     #     #     #     #     #     #       #     #
                        r = s.starts_with(u'\u0bbf\u0bb2\u0bcd\u0bb2\u0bc8')  # character check  ##    #     # or  #     #     #     #     #     #     #     #     #     #     #       #     #
                        wordEnding = 'common_suffix_illai'
                    if not r:                                                                          #     #     # or  #     #     #     #     #     #     #     #     #     #       #     #
                        s.cursor = len(s) - var138                                                     #     #     #     # or  #     #     #     #     #     #     #     #     #       #     #
                        r = s.starts_with(u'\u0bbf\u0b9f\u0bae\u0bcd')  # character check              ##    #     #     #     # or  #     #     #     #     #     #     #     #       #     #
                        wordEnding = 'common_suffix_idam'
                    if not r:                                                                                #     #     #     #     # or  #     #     #     #     #     #     #       #     #
                        s.cursor = len(s) - var139                                                           #     #     #     #     #     # or  #     #     #     #     #     #       #     #
                        r = s.starts_with(u'\u0bbf\u0ba9\u0bcd\u0bb1\u0bbf')  # character check              ##    #     #     #     #     #     # or  #     #     #     #     #       #     #
                        wordEnding = 'common_suffix_inri'
                    if not r:                                                                                      #     #     #     #     #     #     # or  #     #     #     #       #     #
                        s.cursor = len(s) - var140                                                                 #     #     #     #     #     #     #     #     #     #     #       #     #
                        r = s.starts_with(u'\u0bbe\u0b95\u0bbf')  # character check                                ##    #     #     #     #     #     #     #     #     #     #       #     #
                        wordEnding = 'common_suffix_aaki'
                    if not r:                                                                                            #     #     #     #     #     #     #     #     #     #       #     #
                        s.cursor = len(s) - var141                                                                       #     #     #     #     #     #     #     #     #     #       #     #
                        r = s.starts_with(u'\u0bbe\u0b95\u0bbf\u0baf')  # character check                                ##    #     #     #     #     #     #     #     #     #       #     #
                        wordEnding = 'common_suffix_aakiya'
                    if not r:                                                                                                  #     #     #     #     #     #     #     #     #       #     #
                        s.cursor = len(s) - var142                                                                             #     #     #     #     #     #     #     #     #       #     #
                        r = s.starts_with(u'\u0bc6\u0ba9\u0bcd\u0bb1\u0bc1')  # character check                                ##    #     #     #     #     #     #     #     #       #     #
                        wordEnding = 'common_suffix_enru'
                    if not r:                                                                                                        #     #     #     #     #     #     #     #       #     #
                        s.cursor = len(s) - var143                                                                                   #     #     #     #     #     #     #     #       #     #
                        r = s.starts_with(u'\u0bc1\u0bb3\u0bcd\u0bb3')  # character check                                            ##    #     #     #     #     #     #     #       #     #
                        wordEnding = 'common_suffix_ulla'
                    if not r:                                                                                                              #     #     #     #     #     #     #       #     #
                        s.cursor = len(s) - var144                                                                                         #     #     #     #     #     #     #       #     #
                        r = s.starts_with(u'\u0bc1\u0b9f\u0bc8\u0baf')  # character check                                                  ##    #     #     #     #     #     #       #     #
                        wordEnding = 'common_suffix_udaiya'
                    if not r:                                                                                                                    #     #     #     #     #     #       #     #
                        s.cursor = len(s) - var145                                                                                               #     #     #     #     #     #       #     #
                        r = s.starts_with(u'\u0bc1\u0b9f\u0bc8')  # character check                                                              ##    #     #     #     #     #       #     #
                        wordEnding = 'common_suffix_udai'
                    if not r:                                                                                                                          #     #     #     #     #       #     #
                        s.cursor = len(s) - var146                                                                                                     #     # or  #     #     #       #     #
                        r = s.starts_with(u'\u0bc6\u0ba9\u0bc1\u0bae\u0bcd')  # character check                                                        ##    #     # or  #     #       #     #
                        wordEnding = 'common_suffix_enum'
                    if not r:                                                                                                                                #     #     # or  #       #     #
                        s.cursor = len(s) - var156                                                                                                           #     #     #     #       #     #
                        r = s.starts_with(u'\u0bb2\u0bcd\u0bb2')  # character check                                                                          #     #     #     #       #     #
                        wordEnding = 'common_suffix_lla'
                        if r:                                                                                                                                #     #     #     # test  #     #
                            var155 = len(s) - s.cursor                                                                            ##                         #     #     #     #       #     #
                            var154 = len(s) - s.cursor                                                                     ##     #                          #     #     #     #       #     #
                            var153 = len(s) - s.cursor                                                               ##    #      #                          #     #     #     #       #     #
                            var152 = len(s) - s.cursor                                                         ##    #     #      #                          #     #     #     #       #     #
                            var151 = len(s) - s.cursor                                                   ##    #     #     #      #                          #     #     #     #       #     #
                            var150 = len(s) - s.cursor                                             ##    #     #     #     #      #                          #     #     #     #       #     #
                            var149 = len(s) - s.cursor                                       ##    #     #     #     #     #      #                          #     #     #     #       #     #
                            var148 = len(s) - s.cursor                                 ##    #     #     #     #     #     #      #                          #     #     #     #       #     #
                            var147 = len(s) - s.cursor                           ##    #     #     #     #     #     #     #      #                          #     #     #     #       #     #
                            r = s.starts_with(u'\u0bbe')  # character check      #     #     #     #     #     #     #     #      #                          #     #     #     #       #     #
                            if not r:                                            # or  #     #     #     #     #     #     #      #                          #     #     #     #       #     #
                                s.cursor = len(s) - var147                       #     # or  #     #     #     #     #     #      #                          #     #     #     #       #     #
                                r = s.starts_with(u'\u0bbf')  # character check  ##    #     # or  #     #     #     #     #      #                          #     #     #     #       #     #
                            if not r:                                                  #     #     # or  #     #     #     #      #                          #     #     #     #       #     #
                                s.cursor = len(s) - var148                             #     #     #     # or  #     #     #      #                          #     #     #     #       #     #
                                r = s.starts_with(u'\u0bc0')  # character check        ##    #     #     #     # or  #     #      #                          #     #     #     #       #     #
                            if not r:                                                        #     #     #     #     # or  #      #                          #     #     #     #       #     #
                                s.cursor = len(s) - var149                                   #     #     #     #     #     # not  # test                     #     #     #     #       #     #
                                r = s.starts_with(u'\u0bc6')  # character check              ##    #     #     #     #     #      #                          #     #     #     #       #     #
                            if not r:                                                              #     #     #     #     #      #                          #     #     #     #       #     #
                                s.cursor = len(s) - var150                                         #     #     #     #     #      #                          #     #     #     #       #     #
                                r = s.starts_with(u'\u0bc7')  # character check                    ##    #     #     #     #      #                          #     #     #     #       #     #
                            if not r:                                                                    #     #     #     #      #                          #     #     #     #       #     #
                                s.cursor = len(s) - var151                                               #     #     #     #      #                          #     #     #     #       #     #
                                r = s.starts_with(u'\u0bc1')  # character check                          ##    #     #     #      #                          #     #     #     #       #     #
                            if not r:                                                                          #     #     #      #                          #     #     #     #       #     #
                                s.cursor = len(s) - var152                                                     #     #     #      #                          #     #     #     #       #     #
                                r = s.starts_with(u'\u0bc2')  # character check                                ##    #     #      #                          #     #     #     #       #     #
                            if not r:                                                                                #     #      #                          #     #     #     #       #     #
                                s.cursor = len(s) - var153                                                           #     #      #                          #     #     #     #       #     #
                                r = s.starts_with(u'\u0bc8')  # character check                                      ##    #      #                          #     #     #     #       #     #
                            if not r:                                                                                      #      #                          #     #     #     #       #     #
                                s.cursor = len(s) - var154                                                                 #      #                          #     #     #     #       # or  # backwards
                            r = not r                                                                                      ##     #                          #     #     #     #       #     #
                            s.cursor = len(s) - var155                                                                            ##                         ##    #     #     #       #     #
                    if not r:                                                                                                                                      #     #     #       #     #
                        s.cursor = len(s) - var157                                                                                                                 #     #     #       #     #
                        r = s.starts_with(u'\u0bc6\u0ba9')  # character check                                                                                      ##    #     #       #     #
                        wordEnding = 'common_suffix_ena'
                    if not r:                                                                                                                                            #     #       #     #
                        s.cursor = len(s) - var158                                                                                                                       #     #       #     #
                        r = s.starts_with(u'\u0bbe\u0b95\u0bbf')  # character check                                                                                      ##    #       #     #
                        wordEnding = 'common_suffix_aaki'
                    if r:                                                                                                                                                      #       #     #
                        self.right = s.cursor  ##                                                                                                                              #       #     #
                        r = True               ## ]                                                                                                                            #       #     #
                        if r:                                                                                                                                                  #       #     #
                            r = s.set_range(self.left, self.right, u'\u0bcd')  # <-                                                                                            #       #     #
                            s.addSuffix(wordEnding)
                            if r:                                                                                                                                              #       #     #
                                self.b_found_a_match = True  ##                                                                                                                #       #     #
                                r = True                     ## set                                                                                                            #       #     #
                s.cursor = len(s) - var159                                                                                                                                     ##      #     #
                if not r:                                                                                                                                                              #     #
                    s.cursor = len(s) - var174                                                                                                                                         #     #
                    var173 = len(s) - s.cursor                                                                                                                               ##        #     #
                    self.left = s.cursor  ##                                                                                                                                 #         #     #
                    r = True              ## [                                                                                                                               #         #     #
                    if r:                                                                                                                                                    #         #     #
                        var172 = len(s) - s.cursor                                                                                                                     ##    #         #     #
                        var171 = len(s) - s.cursor                                                                                                               ##    #     #         #     #
                        var170 = len(s) - s.cursor                                                                                                         ##    #     #     #         #     #
                        var169 = len(s) - s.cursor                                                                                                   ##    #     #     #     #         #     #
                        var168 = len(s) - s.cursor                                                                                             ##    #     #     #     #     #         #     #
                        var167 = len(s) - s.cursor                                                                                       ##    #     #     #     #     #     #         #     #
                        var166 = len(s) - s.cursor                                                                                 ##    #     #     #     #     #     #     #         #     #
                        var165 = len(s) - s.cursor                                                                           ##    #     #     #     #     #     #     #     #         #     #
                        var164 = len(s) - s.cursor                                                                     ##    #     #     #     #     #     #     #     #     #         #     #
                        var163 = len(s) - s.cursor                                                               ##    #     #     #     #     #     #     #     #     #     #         #     #
                        var162 = len(s) - s.cursor                                                         ##    #     #     #     #     #     #     #     #     #     #     #         #     #
                        var161 = len(s) - s.cursor                                                   ##    #     #     #     #     #     #     #     #     #     #     #     #         #     #
                        var160 = len(s) - s.cursor                                             ##    #     #     #     #     #     #     #     #     #     #     #     #     #         #     #
                        r = s.starts_with(u'\u0baa\u0b9f\u0bc1')  # character check            #     #     #     #     #     #     #     #     #     #     #     #     #     #         #     #
                        wordEnding = 'common_suffix_padu'
                        if not r:                                                              # or  #     #     #     #     #     #     #     #     #     #     #     #     #         #     #
                            s.cursor = len(s) - var160                                         #     # or  #     #     #     #     #     #     #     #     #     #     #     #         #     #
                            r = s.starts_with(u'\u0baa\u0b9f\u0bcd\u0b9f')  # character check  ##    #     # or  #     #     #     #     #     #     #     #     #     #     #         #     #
                            wordEnding = 'common_suffix_patta'
                        if not r:                                                                    #     #     # or  #     #     #     #     #     #     #     #     #     #         #     #
                            s.cursor = len(s) - var161                                               #     #     #     # or  #     #     #     #     #     #     #     #     #         #     #
                            r = s.starts_with(u'\u0baa\u0b9f\u0bcd\u0b9f\u0bc1')  # character check  ##    #     #     #     # or  #     #     #     #     #     #     #     #         #     #
                            wordEnding = 'common_suffix_pattu'
                        if not r:                                                                          #     #     #     #     # or  #     #     #     #     #     #     #         #     #
                            s.cursor = len(s) - var162                                                     #     #     #     #     #     # or  #     #     #     #     #     #         #     #
                            r = s.starts_with(u'\u0baa\u0b9f\u0bcd\u0b9f\u0ba4\u0bc1')  # character check  ##    #     #     #     #     #     # or  #     #     #     #     #         #     #
                            wordEnding = 'common_suffix_pattathu'
                        if not r:                                                                                #     #     #     #     #     #     # or  #     #     #     #         #     #
                            s.cursor = len(s) - var163                                                           #     #     #     #     #     #     #     # or  #     #     #         #     #
                            r = s.starts_with(u'\u0baa\u0b9f\u0bcd\u0b9f\u0ba3')  # character check              ##    #     #     #     #     #     #     #     # or  #     #         #     #
                            wordEnding = 'common_suffix_pattana'
                        if not r:                                                                                      #     #     #     #     #     #     #     #     # or  #         #     #
                            s.cursor = len(s) - var164                                                                 #     #     #     #     #     #     #     #     #     #         #     #
                            r = s.starts_with(u'\u0b95\u0bc1\u0bb0\u0bbf\u0baf')  # character check                    ##    #     #     #     #     #     #     #     #     #         #     #
                            wordEnding = 'common_suffix_kuriya'
                        if not r:                                                                                            #     #     #     #     #     #     #     #     # test    #     #
                            s.cursor = len(s) - var165                                                                       #     #     #     #     #     #     #     #     #         #     #
                            r = s.starts_with(u'\u0b95\u0bc1\u0bb0\u0bbf\u0baf')  # character check                          ##    #     #     #     #     #     #     #     #         #     #
                            wordEnding = 'common_suffix_kuriya'
                        if not r:                                                                                                  #     #     #     #     #     #     #     #         #     #
                            s.cursor = len(s) - var166                                                                             #     #     #     #     #     #     #     #         #     #
                            r = s.starts_with(u'\u0baa\u0bb1\u0bcd\u0bb1\u0bbf')  # character check                                ##    #     #     #     #     #     #     #         #     #
                            wordEnding = 'common_suffix_pattri'
                        if not r:                                                                                                        #     #     #     #     #     #     #         #     #
                            s.cursor = len(s) - var167                                                                                   #     #     #     #     #     #     #         #     #
                            r = s.starts_with(u'\u0bb5\u0bbf\u0b9f\u0bc1')  # character check                                            ##    #     #     #     #     #     #         #     #
                            wordEnding = 'common_suffix_vidu'
                        if not r:                                                                                                              #     #     #     #     #     #         #     #
                            s.cursor = len(s) - var168                                                                                         #     #     #     #     #     #         #     #
                            r = s.starts_with(u'\u0bb5\u0bbf\u0b9f\u0bcd\u0b9f\u0bc1')  # character check                                      ##    #     #     #     #     #         #     #
                            wordEnding = 'common_suffix_vittu'
                        if not r:                                                                                                                    #     #     #     #     #         #     #
                            s.cursor = len(s) - var169                                                                                               #     #     #     #     #         #     #
                            r = s.starts_with(u'\u0baa\u0b9f\u0bbf\u0ba4\u0bbe\u0ba9')  # character check                                            ##    #     #     #     #         #     #
                            wordEnding = 'common_suffix_padithaana'
                        if not r:                                                                                                                          #     #     #     #         #     #
                            s.cursor = len(s) - var170                                                                                                     #     #     #     #         #     #
                            r = s.starts_with(u'\u0baa\u0b9f\u0bbf')  # character check                                                                    ##    #     #     #         #     #
                            wordEnding = 'common_suffix_padi'
                        if not r:                                                                                                                                #     #     #         #     #
                            s.cursor = len(s) - var171                                                                                                           #     #     #         #     #
                            r = s.starts_with(u'\u0ba4\u0bbe\u0ba9')  # character check                                                                          ##    #     #         #     #
                            wordEnding = 'common_suffix_thaana'
                        if not r:                                                                                                                                      #     #         #     #
                            s.cursor = len(s) - var172                                                                                                                 #     #         #     #
                            r = s.starts_with(u'\u0bc6\u0bb2\u0bcd\u0bb2\u0bbe\u0bae\u0bcd')  # character check                                                        ##    #         #     #
                            wordEnding = 'common_suffix_ellaam'

                        if r:                                                                                                                                                #         #     #
                            self.right = s.cursor  ##                                                                                                                        #         #     #
                            r = True               ## ]                                                                                                                      #         #     #
                            if r:                                                                                                                                            #         #     #
                                r = s.set_range(self.left, self.right, u'')  # delete                                                                                        #         #     #
                                s.addSuffix(wordEnding)
                                if r:                                                                                                                                        #         #     #
                                    self.b_found_a_match = True  ##                                                                                                          #         #     #
                                    r = True                     ## set                                                                                                      #         #     #
                    s.cursor = len(s) - var173                                                                                                                               ##        ##    #
                s.direction *= -1                                                                                                                                                            #
                s.cursor = var175                                                                                                                                                            #
                s.limit = len(s) - var176                                                                                                                                                    ##
                if r:
                    var177 = s.cursor                          ##
                    r = self.r_fix_endings(s)  # routine call  #
                    s.cursor = var177                          # do
                    r = True                                   ##
        return r
    
    def r_remove_vetrumai_urupukal(self, s):
        r = True
        self.b_found_a_match = False  ##
        r = True                      ## unset
        if r:
            self.b_found_vetrumai_urupu = False  ##
            r = True                             ## unset
            if r:
                r = self.r_has_min_length(s)  # routine call
                if r:
                    var242 = s.cursor                                                                                                                                                                ##
                    var243 = len(s) - s.limit                                                                                                                                                        #
                    s.direction *= -1                                                                                                                                                                #
                    s.cursor, s.limit = s.limit, s.cursor                                                                                                                                            #
                    var240 = len(s) - s.cursor                                                                                                                                                 ##    #
                    var238 = len(s) - s.cursor                                                                                                                                           ##    #     #
                    var221 = len(s) - s.cursor                                                                                                                                     ##    #     #     #
                    var195 = len(s) - s.cursor                                                                                                  ##                                 #     #     #     #
                    var178 = len(s) - s.cursor                                         ##                                                       #                                  #     #     #     #
                    self.left = s.cursor  ##                                           #                                                        #                                  #     #     #     #
                    r = True              ## [                                         #                                                        #                                  #     #     #     #
                    if r:                                                              #                                                        #                                  #     #     #     #
                        r = s.starts_with(u'\u0ba9\u0bc8')  # character check          #                                                        #                                  #     #     #     #
                        vetrumaiSuffix = "vetrumai_suffix_nai"
                        if r:                                                          # test                                                   #                                  #     #     #     #
                            self.right = s.cursor  ##                                  #                                                        #                                  #     #     #     #
                            r = True               ## ]                                #                                                        #                                  #     #     #     #
                            if r:                                                      #                                                        #                                  #     #     #     #
                                r = s.set_range(self.left, self.right, u'')  # delete  #                                                        #                                  #     #     #     #
                                s.addSuffix(vetrumaiSuffix)
                    s.cursor = len(s) - var178                                         ##                                                       #                                  #     #     #     #
                    if not r:                                                                                                                   #                                  #     #     #     #
                        s.cursor = len(s) - var195                                                                                              #                                  #     #     #     #
                        var194 = len(s) - s.cursor                                                                                      ##      #                                  #     #     #     #
                        self.left = s.cursor  ##                                                                                        #       #                                  #     #     #     #
                        r = True              ## [                                                                                      #       #                                  #     #     #     #
                        if r:                                                                                                           #       #                                  #     #     #     #
                            var193 = len(s) - s.cursor                                                                            ##    #       #                                  #     #     #     #
                            var179 = len(s) - s.cursor                                   ##                                       #     #       #                                  #     #     #     #
                            r = s.starts_with(u'\u0bbf\u0ba9\u0bc8')  # character check  #                                        #     #       #                                  #     #     #     #
                            vetrumaiSuffix = 'vetrumai_suffix_inai'
                            if not r:                                                    # or                                     #     #       #                                  #     #     #     #
                                s.cursor = len(s) - var179                               #                                        #     #       #                                  #     #     #     #
                                r = s.starts_with(u'\u0bc8')  # character check          ##                                       #     #       #                                  #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_ai'
                            if r:                                                                                                 #     #       #                                  #     #     #     #
                                var186 = len(s) - s.cursor                                                                ##      #     #       #                                  #     #     #     #
                                var185 = len(s) - s.cursor                                                         ##     #       #     #       #                                  #     #     #     #
                                var184 = len(s) - s.cursor                                                   ##    #      #       #     #       #                                  #     #     #     #
                                var183 = len(s) - s.cursor                                             ##    #     #      #       #     #       #                                  #     #     #     #
                                var182 = len(s) - s.cursor                                       ##    #     #     #      #       #     #       #                                  #     #     #     #
                                var181 = len(s) - s.cursor                                 ##    #     #     #     #      #       #     #       #                                  #     #     #     #
                                var180 = len(s) - s.cursor                           ##    #     #     #     #     #      #       #     #       #                                  #     #     #     #
                                r = s.starts_with(u'\u0b95')  # character check      #     #     #     #     #     #      #       #     #       #                                  #     #     #     #
                                if not r:                                            # or  #     #     #     #     #      #       #     #       #                                  #     #     #     #
                                    s.cursor = len(s) - var180                       #     # or  #     #     #     #      #       #     #       #                                  #     #     #     #
                                    r = s.starts_with(u'\u0b9a')  # character check  ##    #     # or  #     #     #      #       #     #       #                                  #     #     #     #
                                if not r:                                                  #     #     # or  #     #      #       #     #       #                                  #     #     #     #
                                    s.cursor = len(s) - var181                             #     #     #     # or  #      #       #     #       #                                  #     #     #     #
                                    r = s.starts_with(u'\u0b9f')  # character check        ##    #     #     #     # not  # test  #     #       #                                  #     #     #     #
                                if not r:                                                        #     #     #     #      #       #     #       #                                  #     #     #     #
                                    s.cursor = len(s) - var182                                   #     #     #     #      #       #     #       #                                  #     #     #     #
                                    r = s.starts_with(u'\u0ba4')  # character check              ##    #     #     #      #       #     #       #                                  #     #     #     #
                                if not r:                                                              #     #     #      #       #     #       #                                  #     #     #     #
                                    s.cursor = len(s) - var183                                         #     #     #      #       #     #       # or                               #     #     #     #
                                    r = s.starts_with(u'\u0baa')  # character check                    ##    #     #      #       #     #       #                                  #     #     #     #
                                if not r:                                                                    #     #      #       #     #       #                                  #     #     #     #
                                    s.cursor = len(s) - var184                                               #     #      #       #     #       #                                  #     #     #     #
                                    r = s.starts_with(u'\u0bb1')  # character check                          ##    #      #       #     #       #                                  #     #     #     #
                                if not r:                                                                          #      #       #     #       #                                  #     #     #     #
                                    s.cursor = len(s) - var185                                                     #      #       # or  #       #                                  #     #     #     #
                                r = not r                                                                          ##     #       #     # test  #                                  #     #     #     #
                                s.cursor = len(s) - var186                                                                ##      #     #       #                                  #     #     #     #
                            if not r:                                                                                             #     #       #                                  #     #     #     #
                                s.cursor = len(s) - var193                                                                        #     #       #                                  #     #     #     #
                                r = s.starts_with(u'\u0bc8')  # character check                                                   #     #       #                                  #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_ai'
                                if r:                                                                                             #     #       #                                  #     #     #     #
                                    var192 = len(s) - s.cursor                                                         ##         #     #       #                                  #     #     #     #
                                    var191 = len(s) - s.cursor                                                   ##    #          #     #       #                                  #     #     #     #
                                    var190 = len(s) - s.cursor                                             ##    #     #          #     #       #                                  #     #     #     #
                                    var189 = len(s) - s.cursor                                       ##    #     #     #          #     #       #                                  #     #     #     #
                                    var188 = len(s) - s.cursor                                 ##    #     #     #     #          #     #       #                                  #     #     #     #
                                    var187 = len(s) - s.cursor                           ##    #     #     #     #     #          #     #       #                                  #     #     #     #
                                    r = s.starts_with(u'\u0b95')  # character check      #     #     #     #     #     #          #     #       #                                  #     #     #     #
                                    if not r:                                            # or  #     #     #     #     #          #     #       #                                  #     #     #     #
                                        s.cursor = len(s) - var187                       #     # or  #     #     #     #          #     #       #                                  #     #     #     #
                                        r = s.starts_with(u'\u0b9a')  # character check  ##    #     # or  #     #     #          #     #       #                                  #     #     #     #
                                    if not r:                                                  #     #     # or  #     #          #     #       #                                  #     #     #     #
                                        s.cursor = len(s) - var188                             #     #     #     # or  #          #     #       #                                  #     #     #     #
                                        r = s.starts_with(u'\u0b9f')  # character check        ##    #     #     #     # test     #     #       #                                  #     #     #     #
                                    if not r:                                                        #     #     #     #          #     #       #                                  #     #     #     #
                                        s.cursor = len(s) - var189                                   #     #     #     #          #     #       #                                  #     #     #     #
                                        r = s.starts_with(u'\u0ba4')  # character check              ##    #     #     #          #     #       #                                  #     #     #     #
                                    if not r:                                                              #     #     #          #     #       #                                  #     #     #     #
                                        s.cursor = len(s) - var190                                         #     #     #          #     #       #                                  #     #     #     #
                                        r = s.starts_with(u'\u0baa')  # character check                    ##    #     #          #     #       #                                  #     #     #     #
                                    if not r:                                                                    #     #          #     #       #                                  #     #     #     #
                                        s.cursor = len(s) - var191                                               #     #          #     #       #                                  #     #     #     #
                                        r = s.starts_with(u'\u0bb1')  # character check                          ##    #          #     #       #                                  #     #     #     #
                                    if r:                                                                              #          #     #       #                                  #     #     #     #
                                        r = s.starts_with(u'\u0bcd')  # character check                                #          #     #       #                                  #     #     #     #
                                    s.cursor = len(s) - var192                                                         ##         ##    #       #                                  #     #     #     #
                            if r:                                                                                                       #       #                                  #     #     #     #
                                self.right = s.cursor  ##                                                                               #       #                                  #     #     #     #
                                r = True               ## ]                                                                             #       #                                  #     #     #     #
                                if r:                                                                                                   #       #                                  #     #     #     #
                                    r = s.set_range(self.left, self.right, u'\u0bcd')  # <-                                             #       #                                  #     #     #     #
                                    s.addSuffix(vetrumaiSuffix)
                        s.cursor = len(s) - var194                                                                                      ##      ##                                 #     #     #     #
                    if not r:                                                                                                                                                      #     #     #     #
                        s.cursor = len(s) - var221                                                                                                                                 #     #     #     #
                        var220 = len(s) - s.cursor                                                                                                                         ##      #     #     #     #
                        self.left = s.cursor  ##                                                                                                                           #       #     #     #     #
                        r = True              ## [                                                                                                                         #       #     #     #     #
                        if r:                                                                                                                                              #       #     #     #     #
                            var219 = len(s) - s.cursor                                                                                                               ##    #       #     #     #     #
                            var218 = len(s) - s.cursor                                                                                                         ##    #     #       #     #     #     #
                            var208 = len(s) - s.cursor                                                                                                   ##    #     #     #       #     #     #     #
                            var207 = len(s) - s.cursor                                                                                             ##    #     #     #     #       #     #     #     #
                            var206 = len(s) - s.cursor 
                            var2056 = len(s) - s.cursor
                            var2053 = len(s) - s.cursor                                                                                     ##    #     #     #     #     #       #     #     #     #
                            var205 = len(s) - s.cursor                                                                                 ##    #     #     #     #     #     #       # or  #     #     #
                            var204 = len(s) - s.cursor                                                                           ##    #     #     #     #     #     #     #       #     #     #     #
                            var203 = len(s) - s.cursor                                                                     ##    #     #     #     #     #     #     #     #       #     #     #     #
                            var202 = len(s) - s.cursor                                                               ##    #     #     #     #     #     #     #     #     #       #     #     #     #
                            var201 = len(s) - s.cursor                                                         ##    #     #     #     #     #     #     #     #     #     #       #     #     #     #
                            var198 = len(s) - s.cursor                                                   ##    #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                            var197 = len(s) - s.cursor                                             ##    #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                            var196 = len(s) - s.cursor                                       ##    #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                            r = s.starts_with(u'\u0bca\u0b9f\u0bc1')  # character check      #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                            vetrumaiSuffix = 'vetrumai_suffix_odu'
                            if not r:                                                        # or  #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                s.cursor = len(s) - var196                                   #     # or  #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                r = s.starts_with(u'\u0bcb\u0b9f\u0bc1')  # character check  ##    #     # or  #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_oodu'
                            if not r:                                                              #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                s.cursor = len(s) - var197                                         #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                r = s.starts_with(u'\u0bbf\u0bb2\u0bcd')  # character check        ##    #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_il'
                            if not r:                                                                    #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                s.cursor = len(s) - var198                                               #     # or  #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                r = s.starts_with(u'\u0bbf\u0bb1\u0bcd')  # character check              ##    #     # or  #     #     #     #     #     #     #     #     #       #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_ir'
                            if not r:                                                                          #     #     # or  #     #     #     #     #     #     #     #       #     #     #     #
                                s.cursor = len(s) - var201                                                     #     #     #     # or  #     #     #     #     #     #     #       #     #     #     #
                                r = s.starts_with(u'\u0bbf\u0ba9\u0bcd')  # character check                    #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_in'
                                if r:                                                                          #     #     #     #     # or  #     #     #     #     #     #       #     #     #     #
                                    var200 = len(s) - s.cursor                              ##                 #     #     #     #     #     # or  #     #     #     #     #       #     #     #     #
                                    var199 = len(s) - s.cursor                       ##     #                  #     #     #     #     #     #     # or  #     #     #     #       #     #     #     #
                                    r = s.starts_with(u'\u0bae')  # character check  #      #                  #     #     #     #     #     #     #     # or  #     #     #       #     #     #     #
                                    if not r:                                        # not  # test             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                        s.cursor = len(s) - var199                   #      #                  #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                    r = not r                                        ##     #                  #     #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                    s.cursor = len(s) - var200                              ##                 ##    #     #     #     #     #     #     #     #     #     #       #     #     #     #
                            if not r:                                                                                #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                s.cursor = len(s) - var202                                                           #     #     #     #     #     #     #     #     #     #       #     #     #     #
                                r = s.starts_with(u'\u0bbf\u0ba9\u0bcd\u0bb1\u0bc1')  # character check              ##    #     #     #     #     #     #     #     #     #       #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_inru'
                            if not r:                                                                                      #     #     #     #     #     #     #     #     #       #     #     #     #
                                s.cursor = len(s) - var203                                                                 #     #     #     #     #     #     #     #     #       #     #     #     #
                                r = s.starts_with(u'\u0bbf\u0bb0\u0bc1\u0ba8\u0bcd\u0ba4\u0bc1')  # character check        ##    #     #     #     #     #     #     #     #       #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_irunthu'
                            if not r:                                                                                            #     #     #     #     #     #     #     #       #     #     #     #
                                s.cursor = len(s) - var204                                                                       #     #     #     #     #     #     #     #       #     # or  #     #
                                r = s.starts_with(u'\u0bb5\u0bbf\u0b9f')  # character check                                      ##    #     #     #     #     #     #     #       #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_vida'
                            if not r:                                                                                                  #     #     #     #     #     #     #       #     #     #     #
                                s.cursor = len(s) - var205                                                                             #     #     #     #     #     #     #       #     #     #     #
                                r = self.i_length >= 7  # >=                                                                           #     #     #     #     #     #     #       #     #     #     #
                                if r:                                                                                                  #     #     #     #     #     #     #       #     #     #     #
                                    r = s.starts_with(u'\u0bbf\u0b9f\u0bae\u0bcd')  # character check                                  ##    #     #     #     #     #     #       #     #     # or  #
                                    vetrumaiSuffix = 'vetrumai_suffix_idam'
                            if not r:
                                s.cursor = len(s) - var2053
                                r = s.starts_with(u'\u0bc1\u0b95\u0bcd\u0b95\u0bbe\u0b95') # character check
                                vetrumaiSuffix = 'vetrumai_suffix_ukkaaka'
                            if not r:
                                s.cursor = len(s) - var2056
                                r = s.starts_with('\u0bbe\u0b95')
                                vetrumaiSuffix = 'vetrumai_suffix_aaka'
                            if not r:                                                                                                        #     #     #     # or  #     #       #     #     #     #
                                s.cursor = len(s) - var206                                                                                   #     #     #     #     # or  #       #     #     #     #
                                r = s.starts_with(u'\u0bbe\u0bb2\u0bcd')  # character check                                                  ##    #     #     #     #     # test  #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_aal'
                            if not r:                                                                                                              #     #     #     #     #       #     #     #     #
                                s.cursor = len(s) - var207                                                                                         #     #     #     #     #       #     #     #     #
                                r = s.starts_with(u'\u0bc1\u0b9f\u0bc8')  # character check                                                        ##    #     #     #     #       #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_udai'
                            if not r:                                                                                                                    #     #     #     #       #     #     #     #
                                s.cursor = len(s) - var208                                                                                               #     #     #     #       #     #     #     #
                                r = s.starts_with(u'\u0bbe\u0bae\u0bb2\u0bcd')  # character check                                                        ##    #     #     #       #     #     #     # backwards
                                vetrumaiSuffix = 'vetrumai_suffix_aamal'
                            if not r:                                                                                                                          #     #     #       #     #     #     #
                                s.cursor = len(s) - var218                                                                                                     #     #     #       #     #     #     #
                                r = s.starts_with(u'\u0bb2\u0bcd')  # character check                                                                          #     #     #       #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_l'
                                if r:                                                                                                                          #     #     #       #     #     #     #
                                    var217 = len(s) - s.cursor                                                                            ##                   #     #     #       #     #     #     #
                                    var216 = len(s) - s.cursor                                                                     ##     #                    #     #     #       #     #     #     #
                                    var215 = len(s) - s.cursor                                                               ##    #      #                    #     #     #       #     #     #     #
                                    var214 = len(s) - s.cursor                                                         ##    #     #      #                    #     #     #       #     #     #     #
                                    var213 = len(s) - s.cursor                                                   ##    #     #     #      #                    #     #     #       #     #     #     #
                                    var212 = len(s) - s.cursor                                             ##    #     #     #     #      #                    #     #     #       #     #     #     #
                                    var211 = len(s) - s.cursor                                       ##    #     #     #     #     #      #                    #     #     #       #     #     #     #
                                    var210 = len(s) - s.cursor                                 ##    #     #     #     #     #     #      #                    #     #     #       #     #     #     #
                                    var209 = len(s) - s.cursor                           ##    #     #     #     #     #     #     #      #                    #     #     #       #     #     #     #
                                    r = s.starts_with(u'\u0bbe')  # character check      #     #     #     #     #     #     #     #      #                    #     #     #       #     #     #     #
                                    if not r:                                            # or  #     #     #     #     #     #     #      #                    #     #     #       #     #     #     #
                                        s.cursor = len(s) - var209                       #     # or  #     #     #     #     #     #      #                    #     #     #       #     #     #     #
                                        r = s.starts_with(u'\u0bbf')  # character check  ##    #     # or  #     #     #     #     #      #                    #     #     #       #     #     #     #
                                    if not r:                                                  #     #     # or  #     #     #     #      #                    #     #     #       #     #     #     #
                                        s.cursor = len(s) - var210                             #     #     #     # or  #     #     #      #                    #     #     #       #     #     #     #
                                        r = s.starts_with(u'\u0bc0')  # character check        ##    #     #     #     # or  #     #      #                    #     #     #       #     #     #     #
                                    if not r:                                                        #     #     #     #     # or  #      #                    #     #     #       #     #     #     #
                                        s.cursor = len(s) - var211                                   #     #     #     #     #     # not  # test               #     #     #       #     #     #     #
                                        r = s.starts_with(u'\u0bc6')  # character check              ##    #     #     #     #     #      #                    #     #     #       #     #     #     #
                                    if not r:                                                              #     #     #     #     #      #                    #     #     #       #     #     #     #
                                        s.cursor = len(s) - var212                                         #     #     #     #     #      #                    #     #     #       #     #     #     #
                                        r = s.starts_with(u'\u0bc7')  # character check                    ##    #     #     #     #      #                    #     #     #       #     #     #     #
                                    if not r:                                                                    #     #     #     #      #                    #     #     #       #     #     #     #
                                        s.cursor = len(s) - var213                                               #     #     #     #      #                    #     #     #       #     #     #     #
                                        r = s.starts_with(u'\u0bc1')  # character check                          ##    #     #     #      #                    #     #     #       #     #     #     #
                                    if not r:                                                                          #     #     #      #                    #     #     #       #     #     #     #
                                        s.cursor = len(s) - var214                                                     #     #     #      #                    #     #     #       #     #     #     #
                                        r = s.starts_with(u'\u0bc2')  # character check                                ##    #     #      #                    #     #     #       #     #     #     #
                                    if not r:                                                                                #     #      #                    #     #     #       #     #     #     #
                                        s.cursor = len(s) - var215                                                           #     #      #                    #     #     #       #     #     #     #
                                        r = s.starts_with(u'\u0bc8')  # character check                                      ##    #      #                    #     #     #       #     #     #     #
                                    if not r:                                                                                      #      #                    #     #     #       #     #     #     #
                                        s.cursor = len(s) - var216                                                                 #      #                    #     #     #       #     #     #     #
                                    r = not r                                                                                      ##     #                    #     #     #       #     #     #     #
                                    s.cursor = len(s) - var217                                                                            ##                   ##    #     #       #     #     #     #
                            if not r:                                                                                                                                #     #       #     #     #     #
                                s.cursor = len(s) - var219                                                                                                           #     #       #     #     #     #
                                r = s.starts_with(u'\u0bc1\u0bb3\u0bcd')  # character check                                                                          ##    #       #     #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_ul'
                            if r:                                                                                                                                          #       #     #     #     #
                                self.right = s.cursor  ##                                                                                                                  #       #     #     #     #
                                r = True               ## ]                                                                                                                #       #     #     #     #
                                if r:                                                                                                                                      #       #     #     #     #
                                    r = s.set_range(self.left, self.right, u'\u0bcd')  # <-                                                                                #       #     #     #     #
                                    s.addSuffix(vetrumaiSuffix)
                        s.cursor = len(s) - var220                                                                                                                         ##      ##    #     #     #
                    if not r:                                                                                                                                                            #     #     #
                        s.cursor = len(s) - var238                                                                                                                                       #     #     #
                        var237 = len(s) - s.cursor                                                                                                      ##                               #     #     #
                        self.left = s.cursor  ##                                                                                                        #                                #     #     #
                        r = True              ## [                                                                                                      #                                #     #     #
                        if r:                                                                                                                           #                                #     #     #
                            var236 = len(s) - s.cursor                                                                                            ##    #                                #     #     #
                            var226 = len(s) - s.cursor                                                                     ##                     #     #                                #     #     #
                            var225 = len(s) - s.cursor                                                               ##    #                      #     #                                #     #     #
                            var224 = len(s) - s.cursor                                                         ##    #     #                      #     #                                #     #     #
                            var223 = len(s) - s.cursor                                                   ##    #     #     #                      #     #                                #     #     #
                            var222 = len(s) - s.cursor                                             ##    #     #     #     #                      #     #                                #     #     #
                            r = s.starts_with(u'\u0b95\u0ba3\u0bcd')  # character check            #     #     #     #     #                      #     #                                #     #     #
                            vetrumaiSuffix = 'vetrumai_suffix_kan'
                            if not r:                                                              # or  #     #     #     #                      #     #                                #     #     #
                                s.cursor = len(s) - var222                                         #     # or  #     #     #                      #     #                                #     #     #
                                r = s.starts_with(u'\u0bae\u0bc1\u0ba9\u0bcd')  # character check  ##    #     # or  #     #                      #     #                                #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_mun'
                            if not r:                                                                    #     #     # or  #                      #     #                                #     #     #
                                s.cursor = len(s) - var223                                               #     #     #     # or                   #     #                                #     #     #
                                r = s.starts_with(u'\u0bae\u0bc7\u0bb2\u0bcd')  # character check        ##    #     #     #                      #     #                                #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_meel'
                            if not r:                                                                          #     #     #                      #     #                                #     #     #
                                s.cursor = len(s) - var224                                                     #     #     #                      #     #                                #     #     #
                                r = s.starts_with(u'\u0bae\u0bc7\u0bb1\u0bcd')  # character check              ##    #     #                      #     #                                #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_meer'
                            if not r:                                                                                #     #                      #     #                                #     #     #
                                s.cursor = len(s) - var225                                                           #     #                      #     #                                #     #     #
                                r = s.starts_with(u'\u0b95\u0bc0\u0bb4\u0bcd')  # character check                    ##    #                      #     #                                #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_kiizh'
                            if not r:                                                                                      #                      #     #                                #     #     #
                                s.cursor = len(s) - var226                                                                 #                      #     #                                #     #     #
                                r = s.starts_with(u'\u0baa\u0bbf\u0ba9\u0bcd')  # character check                          ##                     #     #                                #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_pin'
                            if not r:                                                                                                             #     #                                #     #     #
                                s.cursor = len(s) - var236                                                                                        #     #                                #     #     #
                                r = s.starts_with(u'\u0ba4\u0bc1')  # character check                                                             #     #                                #     #     #
                                vetrumaiSuffix = 'vetrumai_suffix_thu'
                                if r:                                                                                                             #     #                                #     #     #
                                    var235 = len(s) - s.cursor                                                                            ##      #     #                                #     #     #
                                    var234 = len(s) - s.cursor                                                                     ##     #       #     #                                #     #     #
                                    var233 = len(s) - s.cursor                                                               ##    #      #       #     #                                #     #     #
                                    var232 = len(s) - s.cursor                                                         ##    #     #      #       #     #                                #     #     #
                                    var231 = len(s) - s.cursor                                                   ##    #     #     #      #       # or  #                                #     #     #
                                    var230 = len(s) - s.cursor                                             ##    #     #     #     #      #       #     # test                           #     #     #
                                    var229 = len(s) - s.cursor                                       ##    #     #     #     #     #      #       #     #                                #     #     #
                                    var228 = len(s) - s.cursor                                 ##    #     #     #     #     #     #      #       #     #                                #     #     #
                                    var227 = len(s) - s.cursor                           ##    #     #     #     #     #     #     #      #       #     #                                #     #     #
                                    r = s.starts_with(u'\u0bbe')  # character check      #     #     #     #     #     #     #     #      #       #     #                                #     #     #
                                    if not r:                                            # or  #     #     #     #     #     #     #      #       #     #                                #     #     #
                                        s.cursor = len(s) - var227                       #     # or  #     #     #     #     #     #      #       #     #                                #     #     #
                                        r = s.starts_with(u'\u0bbf')  # character check  ##    #     # or  #     #     #     #     #      #       #     #                                #     #     #
                                    if not r:                                                  #     #     # or  #     #     #     #      #       #     #                                #     #     #
                                        s.cursor = len(s) - var228                             #     #     #     # or  #     #     #      #       #     #                                #     #     #
                                        r = s.starts_with(u'\u0bc0')  # character check        ##    #     #     #     # or  #     #      #       #     #                                #     #     #
                                    if not r:                                                        #     #     #     #     # or  #      #       #     #                                #     #     #
                                        s.cursor = len(s) - var229                                   #     #     #     #     #     # not  # test  #     #                                #     #     #
                                        r = s.starts_with(u'\u0bc6')  # character check              ##    #     #     #     #     #      #       #     #                                #     #     #
                                    if not r:                                                              #     #     #     #     #      #       #     #                                #     #     #
                                        s.cursor = len(s) - var230                                         #     #     #     #     #      #       #     #                                #     #     #
                                        r = s.starts_with(u'\u0bc7')  # character check                    ##    #     #     #     #      #       #     #                                #     #     #
                                    if not r:                                                                    #     #     #     #      #       #     #                                #     #     #
                                        s.cursor = len(s) - var231                                               #     #     #     #      #       #     #                                #     #     #
                                        r = s.starts_with(u'\u0bc1')  # character check                          ##    #     #     #      #       #     #                                #     #     #
                                    if not r:                                                                          #     #     #      #       #     #                                #     #     #
                                        s.cursor = len(s) - var232                                                     #     #     #      #       #     #                                #     #     #
                                        r = s.starts_with(u'\u0bc2')  # character check                                ##    #     #      #       #     #                                #     #     #
                                    if not r:                                                                                #     #      #       #     #                                #     #     #
                                        s.cursor = len(s) - var233                                                           #     #      #       #     #                                #     #     #
                                        r = s.starts_with(u'\u0bc8')  # character check                                      ##    #      #       #     #                                #     #     #
                                    if not r:                                                                                      #      #       #     #                                #     #     #
                                        s.cursor = len(s) - var234                                                                 #      #       #     #                                #     #     #
                                    r = not r                                                                                      ##     #       #     #                                #     #     #
                                    s.cursor = len(s) - var235                                                                            ##      ##    #                                #     #     #
                            if r:                                                                                                                       #                                #     #     #
                                self.right = s.cursor  ##                                                                                               #                                #     #     #
                                r = True               ## ]                                                                                             #                                #     #     #
                                if r:                                                                                                                   #                                #     #     #
                                    r = s.set_range(self.left, self.right, u'')  # delete                                                               #                                #     #     #
                                    s.addSuffix(vetrumaiSuffix)
                        s.cursor = len(s) - var237                                                                                                      ##                               ##    #     #
                    if not r:                                                                                                                                                                  #     #
                        s.cursor = len(s) - var240                                                                                                                                             #     #
                        var239 = len(s) - s.cursor                                           ##                                                                                                #     #
                        self.left = s.cursor  ##                                             #                                                                                                 #     #
                        r = True              ## [                                           #                                                                                                 #     #
                        if r:                                                                #                                                                                                 #     #
                            r = s.starts_with(u'\u0bc0')  # character check                  #                                                                                                 #     #
                            vetrumaiSuffix = 'vetrumai_suffix_ii'
                            if r:                                                            # test                                                                                            #     #
                                self.right = s.cursor  ##                                    #                                                                                                 #     #
                                r = True               ## ]                                  #                                                                                                 #     #
                                if r:                                                        #                                                                                                 #     #
                                    r = s.set_range(self.left, self.right, u'\u0bbf')  # <-  #                                                                                                 #     #
                                    s.addSuffix(vetrumaiSuffix)
                        s.cursor = len(s) - var239                                           ##                                                                                                ##    #
                    if r:                                                                                                                                                                            #
                        self.b_found_a_match = True  ##                                                                                                                                              #
                        r = True                     ## set                                                                                                                                          #
                        if r:                                                                                                                                                                        #
                            self.b_found_vetrumai_urupu = True  ##                                                                                                                                   #
                            r = True                            ## set                                                                                                                               #
                            if r:                                                                                                                                                                    #
                                var241 = len(s) - s.cursor                                           ##                                                                                              #
                                self.left = s.cursor  ##                                             #                                                                                               #
                                r = True              ## [                                           #                                                                                               #
                                if r:                                                                #                                                                                               #
                                    r = s.starts_with(u'\u0bbf\u0ba9\u0bcd')  # character check      #                                                                                               #
                                    vetrumaiSuffix = 'vetrumai_suffix_in'
                                    if r:                                                            #                                                                                               #
                                        self.right = s.cursor  ##                                    # do                                                                                            #
                                        r = True               ## ]                                  #                                                                                               #
                                        if r:                                                        #                                                                                               #
                                            r = s.set_range(self.left, self.right, u'\u0bcd')  # <-  #                                                                                               #
                                            s.addSuffix(vetrumaiSuffix)
                                s.cursor = len(s) - var241                                           #                                                                                               #
                                r = True                                                             ##                                                                                              #
                    s.direction *= -1                                                                                                                                                                #
                    s.cursor = var242                                                                                                                                                                #
                    s.limit = len(s) - var243                                                                                                                                                        ##
                    if r:
                        var244 = s.cursor                          ##
                        r = self.r_fix_endings(s)  # routine call  #
                        s.cursor = var244                          # do
                        r = True                                   ##
        return r
    
    def r_remove_tense_suffixes(self, s):
        r = True
        self.b_found_a_match = True  ##
        r = True                     ## set
        if r:
            while True:                                                      ##
                var246 = s.cursor                                            #
                r = self.b_found_a_match  # boolean variable check           #
                if r:                                                        #
                    var245 = s.cursor                                  ##    #
                    r = self.r_remove_tense_suffix(s)  # routine call  #     #
                    s.cursor = var245                                  # do  # repeat
                    r = True                                           ##    #
                if not r:                                                    #
                    s.cursor = var246                                        #
                    break                                                    #
            r = True                                                         ##
        return r
    
    def r_remove_tense_suffix(self, s):
        r = True
        self.b_found_a_match = False  ##
        r = True                      ## unset
        if r:
            r = self.r_has_min_length(s)  # routine call
            if r:
                # print('Before any processing: ' + str(s.cursor))
                var333 = s.cursor                                                                                                                                                                                                                                                                                                               ##
                var334 = len(s) - s.limit                                                                                                                                                                                                                                                                                                       #
                s.direction *= -1                                                                                                                                                                                                                                                                                                               #
                s.cursor, s.limit = s.limit, s.cursor                                                                                                                                                                                                                                                                                           #
                var326 = len(s) - s.cursor                                                                                                                                                                                                                                                                                                ##    #
                var325 = len(s) - s.cursor                                                                                                                                                                                                                                                                                          ##    #     #
                var321 = len(s) - s.cursor                                                                                                                                                                                                                                                                                    ##    #     #     #
                var300 = len(s) - s.cursor                                                                                                                                                                                                                                                                              ##    #     #     #     #
                var248 = len(s) - s.cursor                                                                           ##                                                                                                                                                                                                 #     #     #     #     #
                self.left = s.cursor  ##                                                                             #                                                                                                                                                                                                  #     #     #     #     #
                r = True              ## [                                                                           #                                                                                                                                                                                                  #     #     #     #     #
                if r:                                                                                                #                                                                                                                                                                                                  #     #     #     #     #
                    # print('Before checking kondir: ' + str(s.cursor))
                    var247 = len(s) - s.cursor                                                                 ##    #                                                                                                                                                                                                  #     #     #     #     #
                    var12345 = len(s) - s.cursor
                    r = s.starts_with(u'\u0b95\u0bca\u0ba3\u0bcd\u0b9f\u0bbf\u0bb0\u0bcd')  # character check  #     #                                                                                                                                                                                                  #     #     #     #     #
                    tenseSuffix = 'tense_suffix_kondir'
                    # print('After checking kondir: ' + str(s.cursor))
                    if not r:
                        s.cursor = len(s) - var12345
                        r = s.starts_with(u'\u0b95\u0bca\u0ba3\u0bcd\u0b9f\u0bbf\u0bb0\u0bc1') # character check
                        tenseSuffix = 'tense_suffix_kondiru'
                    if not r:                                                                                  # or  #                                                                                                                                                                                                  #     #     #     #     #
                        s.cursor = len(s) - var247                                                             #     #                                                                                                                                                                                                  #     #     #     #     #
                        # print('When checking padu: ' + str(s.cursor))
                        r = s.starts_with(u'\u0baa\u0b9f\u0bc1')  # character check                            ##    #                                                                                                                                                                                                  #     #     #     #     #
                        tenseSuffix = 'tense_suffix_padu'
                    if r:                                                                                            # test                                                                                                                                                                                             #     #     #     #     #
                        self.right = s.cursor  ##                                                                    #                                                                                                                                                                                                  #     #     #     #     #
                        r = True               ## ]                                                                  #                                                                                                                                                                                                  #     #     #     #     #
                        if r:                                                                                        #                                                                                                                                                                                                  #     #     #     #     #
                            r = s.set_range(self.left, self.right, u'')  # delete                                    #                                                                                                                                                                                                  #     #     #     #     #
                            s.addSuffix(tenseSuffix)
                            if r:                                                                                    #                                                                                                                                                                                                  #     #     #     #     #
                                self.b_found_a_match = True  ##                                                      #                                                                                                                                                                                                  #     #     #     #     #
                                r = True                     ## set                                                  #                                                                                                                                                                                                  #     #     #     #     #
                s.cursor = len(s) - var248                                                                           ##                                                                                                                                                                                                 #     #     #     #     #
                if not r:                                                                                                                                                                                                                                                                                               #     #     #     #     #
                    s.cursor = len(s) - var300                                                                                                                                                                                                                                                                          #     #     #     #     #
                    var299 = len(s) - s.cursor                                                                                                                                                                                                                                                                  ##      #     #     #     #     #
                    self.left = s.cursor  ##                                                                                                                                                                                                                                                                    #       #     #     #     #     #
                    r = True              ## [                                                                                                                                                                                                                                                                  #       #     #     #     #     #
                    if r:                                                                                                                                                                                                                                                                                       #       #     #     #     #     #
                        var298 = len(s) - s.cursor                                                                                                                                                                                                                                                        ##    #       #     #     #     #     #
                        var297 = len(s) - s.cursor                                                                                                                                                                                                                                                  ##    #     #       #     #     #     #     #
                        var296 = len(s) - s.cursor                                                                                                                                                                                                                                            ##    #     #     #       #     #     #     #     #
                        var295 = len(s) - s.cursor                                                                                                                                                                                                                                      ##    #     #     #     #       #     #     #     #     #
                        var294 = len(s) - s.cursor                                                                                                                                                                                                                                ##    #     #     #     #     #       #     #     #     #     #
                        var293 = len(s) - s.cursor                                                                                                                                                                                                                          ##    #     #     #     #     #     #       #     #     #     #     #
                        var292 = len(s) - s.cursor                                                                                                                                                                                                                    ##    #     #     #     #     #     #     #       #     #     #     #     #
                        var291 = len(s) - s.cursor                                                                                                                                                                                                              ##    #     #     #     #     #     #     #     #       #     #     #     #     #
                        var290 = len(s) - s.cursor                                                                                                                                                                                                        ##    #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var289 = len(s) - s.cursor                                                                                                                                                                                                  ##    #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var279 = len(s) - s.cursor                                                                                                                                                                                            ##    #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var278 = len(s) - s.cursor                                                                                                                                                                                      ##    #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var277 = len(s) - s.cursor                                                                                                                                                                                ##    #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var276 = len(s) - s.cursor                                                                                                                                                                          ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var275 = len(s) - s.cursor                                                                                                                                                                    ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var274 = len(s) - s.cursor                                                                                                                                                              ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var273 = len(s) - s.cursor                                                                                                                                                        ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var272 = len(s) - s.cursor                                                                                                                                                  ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var271 = len(s) - s.cursor                                                                                                                                            ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var270 = len(s) - s.cursor                                                                                                                                      ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var269 = len(s) - s.cursor                                                                                                                                ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var268 = len(s) - s.cursor                                                                                                                          ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var267 = len(s) - s.cursor                                                                                                                    ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var253 = len(s) - s.cursor                                                                     ##                                             #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var252 = len(s) - s.cursor                                                               ##    #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var251 = len(s) - s.cursor                                                         ##    #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var250 = len(s) - s.cursor                                                   ##    #     #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        var249 = len(s) - s.cursor                                             ##    #     #     #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        r = s.starts_with(u'\u0bae\u0bbe\u0bb0\u0bcd')  # character check      #     #     #     #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        tenseSuffix = 'tense_suffix_maar'
                        if not r:                                                              # or  #     #     #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var249                                         #     # or  #     #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0bae\u0bbf\u0ba9\u0bcd')  # character check  ##    #     # or  #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_min'
                        if not r:                                                                    #     #     # or  #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var250                                               #     #     #     # or                                           #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0ba9\u0bcd')  # character check              ##    #     #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_nan'
                        if not r:                                                                          #     #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var251                                                     #     #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0bbe\u0ba9\u0bcd')  # character check              ##    #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_naan'
                        if not r:                                                                                #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var252                                                           #     #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0bbe\u0bb3\u0bcd')  # character check                    ##    #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_naal'
                        if not r:                                                                                      #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var253                                                                 #                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0bbe\u0bb0\u0bcd')  # character check                          ##                                             #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_naar'
                        if not r:                                                                                                                                     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var267                                                                                                                #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0bb5\u0ba9\u0bcd')  # character check                                                                               #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_van'
                            if r:                                                                                                                                     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var266 = len(s) - s.cursor                                                                                                    ##      #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var265 = len(s) - s.cursor                                                                                             ##     #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var264 = len(s) - s.cursor                                                                                       ##    #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var263 = len(s) - s.cursor                                                                                 ##    #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var262 = len(s) - s.cursor                                                                           ##    #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var261 = len(s) - s.cursor                                                                     ##    #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var260 = len(s) - s.cursor                                                               ##    #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var259 = len(s) - s.cursor                                                         ##    #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var258 = len(s) - s.cursor                                                   ##    #     #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var257 = len(s) - s.cursor                                             ##    #     #     #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var256 = len(s) - s.cursor                                       ##    #     #     #     #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var255 = len(s) - s.cursor                                 ##    #     #     #     #     #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var254 = len(s) - s.cursor                           ##    #     #     #     #     #     #     #     #     #     #     #      #       # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                r = s.starts_with(u'\u0b85')  # character check      #     #     #     #     #     #     #     #     #     #     #     #      #       #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                            # or  #     #     #     #     #     #     #     #     #     #     #      #       #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var254                       #     # or  #     #     #     #     #     #     #     #     #     #      #       #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0b86')  # character check  ##    #     # or  #     #     #     #     #     #     #     #     #      #       #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                  #     #     # or  #     #     #     #     #     #     #     #      #       #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var255                             #     #     #     # or  #     #     #     #     #     #     #      #       #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0b87')  # character check        ##    #     #     #     # or  #     #     #     #     #     #      #       #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                        #     #     #     #     # or  #     #     #     #     #      #       #     #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var256                                   #     #     #     #     #     # or  #     #     #     #      #       #     #     #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0b88')  # character check              ##    #     #     #     #     #     # or  #     #     #      #       #     #     #     #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                              #     #     #     #     #     #     # or  #     #      #       #     #     #     #     #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var257                                         #     #     #     #     #     #     #     # or  #      #       #     #     #     #     #     #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0b89')  # character check                    ##    #     #     #     #     #     #     #     # not  # test  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                                    #     #     #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var258                                               #     #     #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0b8a')  # character check                          ##    #     #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                                          #     #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var259                                                     #     #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0b8e')  # character check                                ##    #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                                                #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var260                                                           #     #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0b8f')  # character check                                      ##    #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                                                      #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var261                                                                 #     #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0b90')  # character check                                            ##    #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                                                            #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var262                                                                       #     #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0b92')  # character check                                                  ##    #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                                                                  #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var263                                                                             #     #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0b93')  # character check                                                        ##    #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                                                                        #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #       # or  #     #     #     #
                                    s.cursor = len(s) - var264                                                                                   #     #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0b94')  # character check                                                              ##    #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                                                                              #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     # or  #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var265                                                                                         #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     # or  #     #     #     #     #       #     #     #     #     #
                                r = not r                                                                                                              ##     #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     # or  #     #     #     #       #     #     #     #     #
                                s.cursor = len(s) - var266                                                                                                    ##      ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     # or  #     #     #       #     #     #     #     #
                        if not r:                                                                                                                                           #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     # or  #     #       #     #     #     #     #
                            s.cursor = len(s) - var268                                                                                                                      #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     # or  #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0bb3\u0bcd')  # character check                                                                                     ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_nal'
                        if not r:                                                                                                                                                 #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var269                                                                                                                            #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     # test  #     #     #     #     #
                            r = s.starts_with(u'\u0bb5\u0bb3\u0bcd')  # character check                                                                                           ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_val'
                        if not r:                                                                                                                                                       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var270                                                                                                                                  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0bb0\u0bcd')  # character check                                                                                                 ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_nar'
                        if not r:                                                                                                                                                             #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var271                                                                                                                                        #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0bb5\u0bb0\u0bcd')  # character check                                                                                                       ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_var'
                        if not r:                                                                                                                                                                   #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var272                                                                                                                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba9')  # character check                                                                                                                         ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_na'
                        if not r:                                                                                                                                                                         #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var273                                                                                                                                                    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0baa')  # character check                                                                                                                               ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_pa'
                        if not r:                                                                                                                                                                               #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var274                                                                                                                                                          #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0b95')  # character check                                                                                                                                     ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_ka'
                        if not r:                                                                                                                                                                                     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var275                                                                                                                                                                #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba4')  # character check                                                                                                                                           ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_tha'
                        if not r:                                                                                                                                                                                           #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var276                                                                                                                                                                      #     #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0baf')  # character check                                                                                                                                                 ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_tha'
                        if not r:                                                                                                                                                                                                 #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var277                                                                                                                                                                            #     #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0baa\u0ba9\u0bcd')  # character check                                                                                                                                           ##    #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_pan'
                        if not r:                                                                                                                                                                                                       #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var278                                                                                                                                                                                  #     #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0baa\u0bb3\u0bcd')  # character check                                                                                                                                                 ##    #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_pal'
                        if not r:                                                                                                                                                                                                             #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var279                                                                                                                                                                                        #     #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0baa\u0bb0\u0bcd')  # character check                                                                                                                                                       ##    #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_par'
                        if not r:                                                                                                                                                                                                                   #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var289                                                                                                                                                                                              #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba4\u0bc1')  # character check                                                                                                                                                                   #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_thu'
                            if r:                                                                                                                                                                                                                   #     #     #     #     #     #     #     #     #     #     #       #     # or  #     #     #
                                var288 = len(s) - s.cursor                                                                            ##                                                                                                            #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var287 = len(s) - s.cursor                                                                     ##     #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var286 = len(s) - s.cursor                                                               ##    #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var285 = len(s) - s.cursor                                                         ##    #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var284 = len(s) - s.cursor                                                   ##    #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var283 = len(s) - s.cursor                                             ##    #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var282 = len(s) - s.cursor                                       ##    #     #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var281 = len(s) - s.cursor                                 ##    #     #     #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                var280 = len(s) - s.cursor                           ##    #     #     #     #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                r = s.starts_with(u'\u0bbe')  # character check      #     #     #     #     #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                            # or  #     #     #     #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     # or  #     #
                                    s.cursor = len(s) - var280                       #     # or  #     #     #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     # do  #
                                    r = s.starts_with(u'\u0bbf')  # character check  ##    #     # or  #     #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                  #     #     # or  #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var281                             #     #     #     # or  #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0bc0')  # character check        ##    #     #     #     # or  #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                        #     #     #     #     # or  #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var282                                   #     #     #     #     #     # not  # test                                                                                                        #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0bc6')  # character check              ##    #     #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                              #     #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var283                                         #     #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0bc7')  # character check                    ##    #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                                    #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var284                                               #     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0bc1')  # character check                          ##    #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                                          #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var285                                                     #     #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0bc2')  # character check                                ##    #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                                                #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     # backwards
                                    s.cursor = len(s) - var286                                                           #     #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    r = s.starts_with(u'\u0bc8')  # character check                                      ##    #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                if not r:                                                                                      #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                    s.cursor = len(s) - var287                                                                 #      #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                r = not r                                                                                      ##     #                                                                                                             #     #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                                s.cursor = len(s) - var288                                                                            ##                                                                                                            ##    #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                        if not r:                                                                                                                                                                                                                         #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var290                                                                                                                                                                                                    #     #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0bbf\u0bb1\u0bcd\u0bb1\u0bc1')  # character check                                                                                                                                                       ##    #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_ittru'
                        if not r:                                                                                                                                                                                                                               #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var291                                                                                                                                                                                                          #     #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0baa\u0bae\u0bcd')  # character check                                                                                                                                                                         ##    #     #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_pam'
                        if not r:                                                                                                                                                                                                                                     #     #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var292                                                                                                                                                                                                                #     #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0bae\u0bcd')  # character check                                                                                                                                                                               ##    #     #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_nam'
                        if not r:                                                                                                                                                                                                                                           #     #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var293                                                                                                                                                                                                                      #     #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba4\u0bc1\u0bae\u0bcd')  # character check                                                                                                                                                                               ##    #     #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_thum'
                        if not r:                                                                                                                                                                                                                                                 #     #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var294                                                                                                                                                                                                                            #     #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0bb1\u0bc1\u0bae\u0bcd')  # character check                                                                                                                                                                                     ##    #     #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_rum'
                        if not r:                                                                                                                                                                                                                                                       #     #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var295                                                                                                                                                                                                                                  #     #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0b95\u0bc1\u0bae\u0bcd')  # character check                                                                                                                                                                                           ##    #     #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_kum'
                        if not r:                                                                                                                                                                                                                                                             #     #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var296                                                                                                                                                                                                                                        #     #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0bc6\u0ba9\u0bcd')  # character check                                                                                                                                                                                                 ##    #     #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_nen'
                        if not r:                                                                                                                                                                                                                                                                   #     #     #       #     #     #     #     #
                            s.cursor = len(s) - var297                                                                                                                                                                                                                                              #     #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0bc8')  # character check                                                                                                                                                                                                                   ##    #     #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_nai'
                        if not r:                                                                                                                                                                                                                                                                         #     #       #     #     #     #     #
                            s.cursor = len(s) - var298                                                                                                                                                                                                                                                    #     #       #     #     #     #     #
                            r = s.starts_with(u'\u0bb5\u0bc8')  # character check                                                                                                                                                                                                                         ##    #       #     #     #     #     #
                            tenseSuffix = 'tense_suffix_vai'
                        if r:                                                                                                                                                                                                                                                                                   #       #     #     #     #     #
                            self.right = s.cursor  ##                                                                                                                                                                                                                                                           #       #     #     #     #     #
                            r = True               ## ]                                                                                                                                                                                                                                                         #       #     #     #     #     #
                            if r:                                                                                                                                                                                                                                                                               #       #     #     #     #     #
                                r = s.set_range(self.left, self.right, u'')  # delete                                                                                                                                                                                                                           #       #     #     #     #     #
                                s.addSuffix(tenseSuffix)
                                if r:                                                                                                                                                                                                                                                                           #       #     #     #     #     #
                                    self.b_found_a_match = True  ##                                                                                                                                                                                                                                             #       #     #     #     #     #
                                    r = True                     ## set                                                                                                                                                                                                                                         #       #     #     #     #     #
                    s.cursor = len(s) - var299                                                                                                                                                                                                                                                                  ##      ##    #     #     #     #
                if not r:                                                                                                                                                                                                                                                                                                     #     #     #     #
                    s.cursor = len(s) - var321                                                                                                                                                                                                                                                                                #     #     #     #
                    var320 = len(s) - s.cursor                                                                                                                                                    ##                                                                                                                          #     #     #     #
                    self.left = s.cursor  ##                                                                                                                                                      #                                                                                                                           #     #     #     #
                    r = True              ## [                                                                                                                                                    #                                                                                                                           #     #     #     #
                    if r:                                                                                                                                                                         #                                                                                                                           #     #     #     #
                        var319 = len(s) - s.cursor                                                                                                                                          ##    #                                                                                                                           #     #     #     #
                        var318 = len(s) - s.cursor                                                                                                                                    ##    #     #                                                                                                                           #     #     #     #
                        var317 = len(s) - s.cursor                                                                                                                              ##    #     #     #                                                                                                                           #     #     #     #
                        var316 = len(s) - s.cursor                                                                                                                        ##    #     #     #     #                                                                                                                           #     #     #     #
                        var315 = len(s) - s.cursor                                                                                                                  ##    #     #     #     #     #                                                                                                                           #     #     #     #
                        var314 = len(s) - s.cursor                                                                                                            ##    #     #     #     #     #     #                                                                                                                           #     #     #     #
                        var313 = len(s) - s.cursor                                                                                                      ##    #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        var312 = len(s) - s.cursor                                                                                                ##    #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        var311 = len(s) - s.cursor                                                                                          ##    #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        var310 = len(s) - s.cursor                                                                                    ##    #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        var309 = len(s) - s.cursor                                                                              ##    #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        var308 = len(s) - s.cursor                                                                        ##    #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        var307 = len(s) - s.cursor                                                                  ##    #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        var306 = len(s) - s.cursor                                                            ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        var305 = len(s) - s.cursor                                                      ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        var304 = len(s) - s.cursor                                                ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        var303 = len(s) - s.cursor                                          ##    #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        r = s.starts_with(u'\u0bbe\u0ba9\u0bcd')  # character check         #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        tenseSuffix = 'tense_suffix_aan'
                        if r:                                                               #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            var302 = len(s) - s.cursor                              ##      #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            var301 = len(s) - s.cursor                       ##     #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0b9a')  # character check  #      #       #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            if not r:                                        # not  # test  # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                                s.cursor = len(s) - var301                   #      #       #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = not r                                        ##     #       #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var302                              ##      #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                        if not r:                                                           #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var303                                      #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0bbe\u0bb3\u0bcd')  # character check     ##    #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_aal'
                        if not r:                                                                 #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var304                                            #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0bbe\u0bb0\u0bcd')  # character check           ##    #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_aar'
                        if not r:                                                                       #     #     #     #     #     #     #     #     # or  #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var305                                                  #     #     #     #     #     #     #     #     #     # or  #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0bc7\u0ba9\u0bcd')  # character check                 ##    #     #     #     #     #     #     #     #     #     # or  #     #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_een'
                        if not r:                                                                             #     #     #     #     #     #     #     #     #     #     # or  #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var306                                                        #     #     #     #     #     #     #     #     #     #     #     # or  #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0bbe')  # character check                                   ##    #     #     #     #     #     #     #     #     #     #     #     # or  #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_aa'
                        if not r:                                                                                   #     #     #     #     #     #     #     #     #     #     #     #     # or  #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var307                                                              #     #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0bbe\u0bae\u0bcd')  # character check                             ##    #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_aam'
                        if not r:                                                                                         #     #     #     #     #     #     #     #     #     #     #     #     # test                                                                                                                      #     #     #     #
                            s.cursor = len(s) - var308                                                                    #     #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0bc6\u0bae\u0bcd')  # character check                                   ##    #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_em'
                        if not r:                                                                                               #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var309                                                                          #     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0bc7\u0bae\u0bcd')  # character check                                         ##    #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_eem'
                        if not r:                                                                                                     #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var310                                                                                #     #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0bcb\u0bae\u0bcd')  # character check                                               ##    #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_oom'
                        if not r:                                                                                                           #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var311                                                                                      #     #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0b95\u0bc1\u0bae\u0bcd')  # character check                                               ##    #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_kum'
                        if not r:                                                                                                                 #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var312                                                                                            #     #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0ba4\u0bc1\u0bae\u0bcd')  # character check                                                     ##    #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_thum'
                        if not r:                                                                                                                       #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var313                                                                                                  #     #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0b9f\u0bc1\u0bae\u0bcd')  # character check                                                           ##    #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_tum'
                        if not r:                                                                                                                             #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var314                                                                                                        #     #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0bb1\u0bc1\u0bae\u0bcd')  # character check                                                                 ##    #     #     #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_rum'
                        if not r:                                                                                                                                   #     #     #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var315                                                                                                              #     #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0bbe\u0baf\u0bcd')  # character check                                                                             ##    #     #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_aay'
                        if not r:                                                                                                                                         #     #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var316                                                                                                                    #     #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0bc6\u0ba9\u0bcd')  # character check                                                                             ##    #     #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_nen'
                        if not r:                                                                                                                                               #     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var317                                                                                                                          #     #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0ba9\u0bbf\u0bb0\u0bcd')  # character check                                                                                   ##    #     #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_nir'
                        if not r:                                                                                                                                                     #     #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var318                                                                                                                                #     #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0bc0\u0bb0\u0bcd')  # character check                                                                                               ##    #     #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_iir'
                        if not r:                                                                                                                                                           #     #                                                                                                                           #     #     #     #
                            s.cursor = len(s) - var319                                                                                                                                      #     #                                                                                                                           #     #     #     #
                            r = s.starts_with(u'\u0bc0\u0baf\u0bb0\u0bcd')  # character check                                                                                               ##    #                                                                                                                           #     #     #     #
                            tenseSuffix = 'tense_suffix_iiyar'
                        if r:                                                                                                                                                                     #                                                                                                                           #     #     #     #
                            self.right = s.cursor  ##                                                                                                                                             #                                                                                                                           #     #     #     #
                            r = True               ## ]                                                                                                                                           #                                                                                                                           #     #     #     #
                            if r:                                                                                                                                                                 #                                                                                                                           #     #     #     #
                                r = s.set_range(self.left, self.right, u'\u0bcd')  # <-                                                                                                           #                                                                                                                           #     #     #     #
                                s.addSuffix(tenseSuffix)
                                if r:                                                                                                                                                             #                                                                                                                           #     #     #     #
                                    self.b_found_a_match = True  ##                                                                                                                               #                                                                                                                           #     #     #     #
                                    r = True                     ## set                                                                                                                           #                                                                                                                           #     #     #     #
                    s.cursor = len(s) - var320                                                                                                                                                    ##                                                                                                                          ##    #     #     #
                if not r:                                                                                                                                                                                                                                                                                                           #     #     #
                    s.cursor = len(s) - var325                                                                                                                                                                                                                                                                                      #     #     #
                    var324 = len(s) - s.cursor                                           ##                                                                                                                                                                                                                                         #     #     #
                    self.left = s.cursor  ##                                             #                                                                                                                                                                                                                                          #     #     #
                    r = True              ## [                                           #                                                                                                                                                                                                                                          #     #     #
                    if r:                                                                #                                                                                                                                                                                                                                          #     #     #
                        var322 = len(s) - s.cursor                                 ##    #                                                                                                                                                                                                                                          #     #     #
                        r = s.starts_with(u'\u0b95\u0bc1')  # character check      #     #                                                                                                                                                                                                                                          #     #     #
                        tenseSuffix = 'tense_suffix_kku'
                        if not r:                                                  # or  #                                                                                                                                                                                                                                          #     #     #
                            s.cursor = len(s) - var322                             #     #                                                                                                                                                                                                                                          #     #     #
                            r = s.starts_with(u'\u0ba4\u0bc1')  # character check  ##    #                                                                                                                                                                                                                                          #     #     #
                            tenseSuffix = 'tense_suffix_ththu'
                    if r:                                                                #                                                                                                                                                                                                                                          #     #     #
                        var323 = len(s) - s.cursor                       ##              #                                                                                                                                                                                                                                          #     #     #
                        r = s.starts_with(u'\u0bcd')  # character check  # test          # test                                                                                                                                                                                                                                     #     #     #
                        s.cursor = len(s) - var323                       ##              #                                                                                                                                                                                                                                          #     #     #
                        if r:                                                            #                                                                                                                                                                                                                                          #     #     #
                            self.right = s.cursor  ##                                    #                                                                                                                                                                                                                                          #     #     #
                            r = True               ## ]                                  #                                                                                                                                                                                                                                          #     #     #
                            if r:                                                        #                                                                                                                                                                                                                                          #     #     #
                                r = s.set_range(self.left, self.right, u'')  # delete    #                                                                                                                                                                                                                                          #     #     #
                                s.addSuffix(tenseSuffix)
                                if r:                                                    #                                                                                                                                                                                                                                          #     #     #
                                    self.b_found_a_match = True  ##                      #                                                                                                                                                                                                                                          #     #     #
                                    r = True                     ## set                  #                                                                                                                                                                                                                                          #     #     #
                    s.cursor = len(s) - var324                                           ##                                                                                                                                                                                                                                         ##    #     #
                s.cursor = len(s) - var326                                                                                                                                                                                                                                                                                                #     #
                r = True                                                                                                                                                                                                                                                                                                                  ##    #
                if r:                                                                                                                                                                                                                                                                                                                           #
                    var332 = len(s) - s.cursor                                                                                                 ##                                                                                                                                                                                               #
                    self.left = s.cursor  ##                                                                                                   #                                                                                                                                                                                                #
                    r = True              ## [                                                                                                 #                                                                                                                                                                                                #
                    if r:                                                                                                                      #                                                                                                                                                                                                #
                        var331 = len(s) - s.cursor                                                                                       ##    #                                                                                                                                                                                                #
                        var330 = len(s) - s.cursor                                                                                 ##    #     #                                                                                                                                                                                                #
                        var329 = len(s) - s.cursor                                                                           ##    #     #     #                                                                                                                                                                                                #
                        var328 = len(s) - s.cursor                                                                     ##    #     #     #     #                                                                                                                                                                                                #
                        var327 = len(s) - s.cursor                                                               ##    #     #     #     #     #                                                                                                                                                                                                #
                        r = s.starts_with(u'\u0bbe\u0ba8\u0bbf\u0ba9\u0bcd\u0bb1')  # character check            #     #     #     #     #     #                                                                                                                                                                                                #
                        tenseSuffix = 'tense_suffix_aaninra'
                        if not r:                                                                                # or  #     #     #     #     #                                                                                                                                                                                                #
                            s.cursor = len(s) - var327                                                           #     # or  #     #     #     #                                                                                                                                                                                                #
                            r = s.starts_with(u'\u0bbe\u0ba8\u0bbf\u0ba9\u0bcd\u0bb1\u0bcd')  # character check  ##    #     # or  #     #     #                                                                                                                                                                                                #
                            tenseSuffix = 'tense_suffix_aaninr'
                        if not r:                                                                                      #     #     # or  #     #                                                                                                                                                                                                #
                            s.cursor = len(s) - var328                                                                 #     #     #     # or  #                                                                                                                                                                                                #
                            r = s.starts_with(u'\u0b95\u0bbf\u0ba9\u0bcd\u0bb1')  # character check                    ##    #     #     #     #                                                                                                                                                                                                #
                            tenseSuffix = 'tense_suffix_kinra'
                        if not r:                                                                                            #     #     #     #                                                                                                                                                                                                #
                            s.cursor = len(s) - var329                                                                       #     #     #     # do                                                                                                                                                                                             #
                            r = s.starts_with(u'\u0b95\u0bbf\u0ba9\u0bcd\u0bb1\u0bcd')  # character check                    ##    #     #     #                                                                                                                                                                                                #
                            tenseSuffix = 'tense_suffix_kinr'
                        if not r:                                                                                                  #     #     #                                                                                                                                                                                                #
                            s.cursor = len(s) - var330                                                                             #     #     #                                                                                                                                                                                                #
                            r = s.starts_with(u'\u0b95\u0bbf\u0bb1')  # character check                                            ##    #     #                                                                                                                                                                                                #
                            tenseSuffix = 'tense_suffix_kira'
                        if not r:                                                                                                        #     #                                                                                                                                                                                                #
                            s.cursor = len(s) - var331                                                                                   #     #                                                                                                                                                                                                #
                            r = s.starts_with(u'\u0b95\u0bbf\u0bb1\u0bcd')  # character check                                            ##    #                                                                                                                                                                                                #
                            tenseSuffix = 'tense_suffix_kir'
                        if r:                                                                                                                  #                                                                                                                                                                                                #
                            self.right = s.cursor  ##                                                                                          #                                                                                                                                                                                                #
                            r = True               ## ]                                                                                        #                                                                                                                                                                                                #
                            if r:                                                                                                              #                                                                                                                                                                                                #
                                r = s.set_range(self.left, self.right, u'')  # delete                                                          #                                                                                                                                                                                                #
                                s.addSuffix(tenseSuffix)
                                if r:                                                                                                          #                                                                                                                                                                                                #
                                    self.b_found_a_match = True  ##                                                                            #                                                                                                                                                                                                #
                                    r = True                     ## set                                                                        #                                                                                                                                                                                                #
                    s.cursor = len(s) - var332                                                                                                 #                                                                                                                                                                                                #
                    r = True                                                                                                                   ##                                                                                                                                                                                               #
                s.direction *= -1                                                                                                                                                                                                                                                                                                               #
                s.cursor = var333                                                                                                                                                                                                                                                                                                               #
                s.limit = len(s) - var334                                                                                                                                                                                                                                                                                                       ##
                if r:
                    var335 = s.cursor                          ##
                    r = self.r_fix_endings(s)  # routine call  #
                    s.cursor = var335                          # do
                    r = True                                   ##
        return r
    
    def r_stem(self, s):
        r = True
        var336 = s.cursor                         ##
        r = self.r_fix_ending(s)  # routine call  #
        s.cursor = var336                         # do
        r = True                                  ##
        if r:
            r = self.r_has_min_length(s)  # routine call
            if r:
                var337 = s.cursor                                       ##
                r = self.r_remove_question_prefixes(s)  # routine call  #
                s.cursor = var337                                       # do
                r = True                                                ##
                if r:
                    var338 = s.cursor                                      ##
                    r = self.r_remove_pronoun_prefixes(s)  # routine call  #
                    s.cursor = var338                                      # do
                    r = True                                               ##
                    if r:
                        var339 = s.cursor                                       ##
                        r = self.r_remove_question_suffixes(s)  # routine call  #
                        s.cursor = var339                                       # do
                        r = True                                                ##
                        if r:
                            var340 = s.cursor                        ##
                            r = self.r_remove_um(s)  # routine call  #
                            s.cursor = var340                        # do
                            r = True                                 ##
                            if r:
                                var341 = s.cursor                                         ##
                                r = self.r_remove_common_word_endings(s)  # routine call  #
                                s.cursor = var341                                         # do
                                r = True                                                  ##
                                if r:
                                    var342 = s.cursor                                       ##
                                    r = self.r_remove_vetrumai_urupukal(s)  # routine call  #
                                    s.cursor = var342                                       # do
                                    r = True                                                ##
                                    if r:
                                        var343 = s.cursor                                   ##
                                        r = self.r_remove_plural_suffix(s)  # routine call  #
                                        s.cursor = var343                                   # do
                                        r = True                                            ##
                                        if r:
                                            var344 = s.cursor                                      ##
                                            r = self.r_remove_command_suffixes(s)  # routine call  #
                                            s.cursor = var344                                      # do
                                            r = True                                               ##
                                            if r:
                                                var345 = s.cursor                                    ##
                                                r = self.r_remove_tense_suffixes(s)  # routine call  #
                                                s.cursor = var345                                    # do
                                                r = True                                             ##
        return r
