/*
 * Copyright (c) 1987, 1988, 1989, 1990, 1991 Stanford University
 * Copyright (c) 1991 Silicon Graphics, Inc.
 *
 * Permission to use, copy, modify, distribute, and sell this software and 
 * its documentation for any purpose is hereby granted without fee, provided
 * that (i) the above copyright notices and this permission notice appear in
 * all copies of the software and related documentation, and (ii) the names of
 * Stanford and Silicon Graphics may not be used in any advertising or
 * publicity relating to the software without the specific, prior written
 * permission of Stanford and Silicon Graphics.
 * 
 * THE SOFTWARE IS PROVIDED "AS-IS" AND WITHOUT WARRANTY OF ANY KIND, 
 * EXPRESS, IMPLIED OR OTHERWISE, INCLUDING WITHOUT LIMITATION, ANY 
 * WARRANTY OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  
 *
 * IN NO EVENT SHALL STANFORD OR SILICON GRAPHICS BE LIABLE FOR
 * ANY SPECIAL, INCIDENTAL, INDIRECT OR CONSEQUENTIAL DAMAGES OF ANY KIND,
 * OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
 * WHETHER OR NOT ADVISED OF THE POSSIBILITY OF DAMAGE, AND ON ANY THEORY OF 
 * LIABILITY, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE 
 * OF THIS SOFTWARE.
 */

/*
 * ScrollBar - simple scrolling interface.
 */

#ifndef ivlook2_6_scrollbar_h
#define ivlook2_6_scrollbar_h

#include <IV-2_6/InterViews/scene.h>

#include <IV-2_6/_enter.h>

class ScrollBar : public MonoScene {
protected:
    Interactor* interactor;
    int size;

    ScrollBar(Interactor*, int);
    ScrollBar(const char*, Interactor*, int);
    virtual ~ScrollBar();

    void Use(Interactor*);
};

class HScrollBar : public ScrollBar {
public:
    HScrollBar(Interactor*, int size = 0);
    HScrollBar(const char*, Interactor*, int size = 0);
    virtual ~HScrollBar();

    virtual void Reconfig();
private:
    void Init();
};

class VScrollBar : public ScrollBar {
public:
    VScrollBar(Interactor*, int size = 0);
    VScrollBar(const char*, Interactor*, int size = 0);
    virtual ~VScrollBar();

    virtual void Reconfig();
private:
    void Init();
};

#include <IV-2_6/_leave.h>

#endif
