#import "@preview/tablex:0.0.4": tablex, rowspanx, colspanx

#import "typst-stringify.typ": stringify

// XXX some of these are ignored, e.g. authors and abstract
#let conf(
  title: none,
  authors: none,
  date: none,
  abstract: none,
  cols: 1,
  margin: (x: 1.25in, y: 1.25in),
  paper: "us-letter",
  lang: "en",
  region: "US",
  font: (),
  fontsize: 11pt,
  sectionnumbering: none,
  info: (),
  doc,
) = {
  // these can be set as metadata or variables
  let figure-numbering = info.at("figure-numbering", default: false)
  let hyphenate = info.at("hyphenate", default: true)
  let justify = info.at("justify", default: false)

  ///////////////
  // begin styles

  // XXX I couldn't work out how to put these in a separate file
  //     should check https://typst.app/docs/tutorial/
  //                      making-a-template#set-and-show-rules

  // pagebreak() can only be used at the outer level
  show <cls:new-page>: it => {
    pagebreak(weak: true)
    it
  }

  // XXX this hides content but it still occupies space; is there
  //     an equivalent of CSS display: none?
  show <cls:hidden>: it => hide(it)

  // XXX can't use .or() with label selectors so have to repeat?
  show <cls:annex1>: it => {
    pagebreak(weak: true)
    it
  }

  // XXX can't use .or() with label selectors so have to repeat?
  show <cls:appendix1>: it => {
    pagebreak(weak: true)
    it
  }

  // XXX setting weak to true suppresses the vertical space
  show heading.where(level: 1): it => {
    v(1em, weak: false)
    it
  }

  // XXX the overall width is wrong when there's no icon
  let alert(width: 100%, inset: 0.5em, radius: 0.3em, color: black,
      gutter: 0.8em, icon: none, iheight: 0.8em, label: none, body) = {
    let fcolor = color.lighten(90%)
    let scolor = color.lighten(50%)
    set block(width: width, inset: inset, radius: radius, fill: fcolor)

    set image(height: iheight)
    let thumb = if icon != none {image(icon)} else {none}

    let cgutt = if thumb != none {gutter} else {0.0em}
    set grid(columns: 2, gutter: gutter, column-gutter: cgutt)

    if label == none {
      block(stroke: scolor, grid(thumb, body))
    } else {
      block(stroke: scolor, grid(thumb, label, none, body))
    }
  }

  show block.where(label: <cls:bug>): it => {
    alert(color: yellow, icon: "bee.png", iheight: 2.0em, it)
  }

  show block.where(label: <cls:note>): it => {
    alert(color: blue, icon: "pencil.png", it)
  }

  show block.where(label: <cls:see-also>): it => {
    alert(color: green, icon: "right.png", label: [*See also:*], it)
  }

  show block.where(label: <cls:tip>): it => {
    alert(color: red, icon: "tick.png", it)
  }

  set outline(indent: 1em)

  show outline.entry.where(level: 1): it => {
    // XXX can this be done via .where()?
    if it.element.func() == heading {
      v(12pt, weak: true)
      strong(it)
    } else [
      #let location = it.element.location()
      #link(location)[
        #if figure-numbering [#it.body] else [#it.element.caption]]
      #box(width: 1fr, repeat[.])
      #link(location)[#it.page]
    ]
  }

  set outline(indent: 1em)

  show outline.entry.where(level: 1): it => {
    // XXX can this be done via .where()?
    if it.element.func() == heading {
      v(12pt, weak: true)
      strong(it)
    } else [
      #let location = it.element.location()
      #link(location)[
        #if figure-numbering [#it.body] else [#it.element.caption]]
      #box(width: 1fr, repeat[.])
      #link(location)[#it.page]
    ]
  }

  show figure: it => align(left)[
    #let body-at-top = (it.kind != table)
    #v(15pt, weak: true)
    #if body-at-top {it.body}
    #v(10pt, weak: true)
    #[
      #set align(center)
      *#if figure-numbering [#it.supplement
           #it.counter.display(it.numbering):] #it.caption*
    ]
    #v(10pt, weak: true)
    #if not body-at-top {it.body}
    #v(15pt, weak: true)
  ]

  show raw.where(block: true): it => {
    set text(size: 0.9em)
    it
  }

  // these are for bibliographic references
  // XXX the fractional widths should be customizable
  show <cls:csl-bib-body>: set block(spacing: 0.25em)

  show <cls:csl-left-margin>: it => box(width: 1fr, baseline: 100%, it)

  show <cls:csl-right-inline>: it => box(width: 15fr, baseline: 100%, it)

  /*
  // XXX this is disabled until can resolve the issues listed below

  set footnote.entry(gap: 0.8em)

  // this is needed because the default doesn't handle blocks well (the
  // second and subsequent lines aren't indented
  // XXX but it doesn't work, because the footnote references are broken
  // XXX could add a link back, but not worth it because it's the same page
  show footnote.entry: it => {
    set box(baseline: 100%)
    let loc = it.note.location()
    let number = counter(footnote).at(loc)
    box[#super[#number.at(0)]]
    h(0.2em)
    box(it.note.body)
  }
  */

  // end styles
  /////////////

  // set the document properties
  // XXX if authors is an array, we should pass an array
  set document(
    title: stringify(title),
    author: stringify(authors)
  )

  // the various bbfXxx variables are passed via the info variable
  let bbf-contrib = info.bbfContrib
  let bbf-issue = info.bbfIssue
  let bbf-month = info.bbfMonth
  let bbf-number = info.bbfNumber
  let bbf-status = info.bbfStatus
  let bbf-title = info.bbfTitle
  let bbf-type = info.bbfType
  let bbf-version = info.bbfVersion
  let bbf-year = info.bbfYear

  // the copyright is fixed text
  let copyright = [#sym.copyright The Broadband Forum. All rights reserved]

  // set the page properties
  set page(
    paper: paper,
    margin: margin,
    background: 2 *
      stack(
        v(15.0em),
        rotate(-40deg, text(
          72pt, fill: black.lighten(90%), smallcaps(bbf-status))),
        v(15.0em)
      ),
    header: locate(loc => {
      set text(size: 0.9em)
      if loc.page() > 1 [#bbf-title #h(1fr) #bbf-number]
    }),
    footer: locate(loc => {
      set text(size: 0.9em)
      [
        #if loc.page() > 1 [#bbf-month #bbf-year]
        #h(1fr) #copyright #h(1fr)
        #if loc.page() > 1 [#counter(page).display("1 of 1", both: true)]
      ]
    })
  )

  show link: underline

  set par(justify: justify)

  set text(lang: lang,
           region: region,
           font: font,
           size: fontsize,
           hyphenate: hyphenate)

  set heading(numbering: sectionnumbering)

  // cover page
  page[
    #set text(weight: "bold", size: 1.5em)
    #stack(
      image("broadband-forum-logo.png", width: 50%),
      v(0.5em),
      smallcaps(bbf-type),
      v(2em),
      [
        #set align(center)
        #stack(
          smallcaps(bbf-status),
          v(1.0em),
          if bbf-contrib != [] {
            link("https://issues.broadband-forum.org/browse/" +
                    stringify(bbf-contrib), bbf-contrib)}
        )
      ],
      v(7.0em),
      [
        #set align(right)
        #stack(
          bbf-number,
          v(0.5em),
          bbf-title,
          v(1.0em),
          [
            #set text(weight: "regular", size: 0.8em)
            #stack(
              if bbf-version != [] [#bbf-issue: #bbf-version],
              v(0.5em),
              [#bbf-month #bbf-year]
            )
          ]
        )
      ]
    )
  ]

  if cols == 1 {
    doc
  } else {
    columns(cols, doc)
  }
}
