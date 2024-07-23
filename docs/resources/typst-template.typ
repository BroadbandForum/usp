#import "typst-stringify.typ": stringify

// XXX should filter out things that need to be ignored
#let bbf-passthrough(content) = { content }

// XXX this should pick up the release info
#let bbf-release = bbf-passthrough
#let bbf-new-file = bbf-passthrough
#let bbf-same-file = bbf-passthrough
#let bbf-same-section = bbf-passthrough
// XXX might need to convert this to vertical space
#let bbf-spacer = bbf-passthrough

// pagebreak() can only be used at the outer level
#let bbf-new-page(content) = { pagebreak(weak: true); content }

// acknowledgments, editors etc.
#let bbf-acknowledgments = bbf-passthrough
#let bbf-editors = bbf-passthrough
#let bbf-issue-history = bbf-passthrough
#let bbf-revision-history = bbf-passthrough

// PSLs and WADs
#let bbf-psls = bbf-passthrough
#let bbf-wads = bbf-passthrough

// annexes
#let bbf-annex1 = bbf-new-page
#let bbf-annex2 = bbf-passthrough
#let bbf-annex3 = bbf-passthrough
#let bbf-annex4 = bbf-passthrough
#let bbf-annex5 = bbf-passthrough
#let bbf-annex6 = bbf-passthrough
#let bbf-annex = bbf-passthrough

// appendices
#let bbf-appendix1 = bbf-new-page
#let bbf-appendix2 = bbf-passthrough
#let bbf-appendix3 = bbf-passthrough
#let bbf-appendix4 = bbf-passthrough
#let bbf-appendix5 = bbf-passthrough
#let bbf-appendix6 = bbf-passthrough
#let bbf-appendix = bbf-passthrough

// bibliographic references
// XXX the fractional widths should be customizable
#let bbf-nocase = bbf-passthrough
#let bbf-references = bbf-passthrough
#let bbf-csl-entry = bbf-passthrough
#let bbf-csl-bib-body = block.with(spacing: 0.25em)
#let bbf-csl-left-margin = box.with(width: 1fr, baseline: 100%)
#let bbf-csl-right-inline = box.with(width: 15fr, baseline: 100%)

// left / right / clear (intended for use with divs)
#let bbf-left-state = state("bbf-left")
#let bbf-right-state = state("bbf-right")

#let bbf-left = content => state("bbf-left").update(content)
#let bbf-right = content => state("bbf-right").update(content)

#let bbf-clear = (..args) => {
  set table(columns: (50%, 50%), stroke: 1pt + black.lighten(95%),
            ..args.named())
  locate(loc => {
    let left_content = state("bbf-left").at(loc)
    let right_content = state("bbf-right").at(loc)
    if left_content != none and right_content != none {
      table(left_content, right_content)
    }
  })
  bbf-left(none)
  bbf-right(none)
  args.pos().join()
}

// table support
#let bbf-table-chain(obj, ..opts) = {
  if type(obj) == content {
    table.cell(obj, ..opts)
  } else {
    // it's expected to be a dictionary
    assert.eq(opts.pos(), ())
    obj + opts.named()
  }
}

// XXX these are rather arbitrary
#let bbf-table-blue = obj => bbf-table-chain(obj, fill: blue.lighten(50%))
#let bbf-table-red = obj => bbf-table-chain(obj, fill: red.lighten(50%))
#let bbf-table-right = obj => bbf-table-chain(obj, align: right)

// WT-181/specification/local.css
#let bbf-table-command = table.cell.with(fill: rgb("#66cdaa"))
#let bbf-table-object = table.cell.with(fill: rgb("#ffff99"))

// WT-124
#let bbf-requirements-table = bbf-passthrough

// XXX maybe there's a better solution for things like the following

// XXX this hides content but it still occupies space; is there
//     an equivalent of CSS 'display: none'?
#let bbf-hidden = hide

// XXX this assumes a box rather than a block
#let bbf-gray = box.with(fill: gray.lighten(50%))

// XXX is there a more idiomatic way of doing this?
#let bbf-emphasis(content) = { emph(content) }

#let bbf-raw-size = 0.8em
#let bbf-raw-font = ("Courier New", "Courier", "Liberation Mono", "monospace")
#let bbf-code(content) = { set text(size: bbf-raw-size, font: bbf-raw-font);
                           content}
// XXX need to review this
#let bbf-ebnf = bbf-code

// XXX using spacing here should be the same, but it doesn't seem to work
#let bbf-nobreak = block.with(breakable: false, above: 0.6em, below: 0.6em)

// alerts
#let bbf-alert(width: 100%, inset: 0.5em, radius: 0.3em, color: black,
               gutter: 0.8em, icon: none, iheight: 0.8em, label: none,
               content) = {
  let fcolor = color.lighten(95%)
  let scolor = color.lighten(60%)
  set block(width: width, inset: inset, radius: radius, fill: fcolor,
            stroke: scolor)

  set image(height: iheight)
  let thumb = if icon != none {image(icon)} else {none}

  let cgutt = if thumb != none {gutter} else {0.0em}
  set grid(columns: 2, gutter: gutter, column-gutter: cgutt)

  let hfill = [#h(1fr)]

  if label == none {
    block(grid(thumb, content + hfill))
  } else {
    block(grid(thumb, label, none, content + hfill))
  }
}

#let bbf-bug = bbf-alert.with(color: yellow, icon: "bee.png", iheight: 2.0em)
#let bbf-note = bbf-alert.with(color: blue, icon: "pencil.png")
#let bbf-see-also = bbf-alert.with(color: green, icon: "right.png",
                                   label: [*See also:*])
#let bbf-tip = bbf-alert.with(color: red, icon: "tick.png")

// table styling

#let bbf-nosidelines(content) = {
  set table(stroke: (x, y) => {
      let style = 1pt + black
      (top: style, bottom: style)
      if x > 0 {
        (left: style)
      }
    }
  )
  content
}

#let bbf-borderless(content) = {
  set table(stroke: none)
  content
}

#let bbf-boldfirst(content) = {
  show table.cell.where(x: 0): strong
  content
}

// XXX some of these are ignored, e.g. authors and abstract
#let conf(
  title: none,
  authors: none,
  date: none,
  abstract: none,
  cols: 1,
  margin: auto,
  paper: "us-letter",
  lang: "en",
  region: "US",
  font: ("Arial", "Liberation Sans", "Nimbus Sans", "DejaVu Sans"),
  fontsize: 10pt,
  sectionnumbering: none,
  info: (),
  doc,
) = {

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

  // these can be set as metadata or variables
  let figure-numbering = info.at("figure-numbering", default: false)
  let hyphenate = info.at("hyphenate", default: false)
  let justify = info.at("justify", default: true)

  // these approximate the WT-210 recommendations
  show heading: set block(above: 18pt, below: 12pt)
  show par: set block(spacing: 12pt)

  show heading.where(level: 1): set text(size: fontsize * 2.0)
  show heading.where(level: 2): set text(size: fontsize * 1.5)
  show heading.where(level: 3): set text(size: fontsize * 1.2)
  show heading.where(level: 4): set text(size: fontsize * 1.2)
  show heading.where(level: 5): set text(size: fontsize * 1.2)
  show heading.where(level: 6): set text(size: fontsize * 1.2)

  // TOOLS-193: Headings are colored in WT-210 using the color #204F57
  // (sort of dark petrol color)
  show heading: set text(fill: rgb("#204F57"))

  // TOOLS-200: list indent and bullet style
  // XXX the second two might need to be moved up or scaled?
  set list(indent: 1em)
  set list(marker: (sym.circle.filled, sym.circle.stroked.small,
                    sym.square.filled.tiny, sym.circle.filled.small,
                    sym.circle.stroked.tiny))

  // XXX these are rather small
  let bullet = str.from-unicode(0x2022)
  let white-bullet = str.from-unicode(0x25E6)
  let black-very-small-square = str.from-unicode(0x2B1D)
  //#set list(marker: (bullet, white-bullet, black-very-small-square))

  // TOOLS-201: do the same for figure captions
  show figure.caption: set text(fill: rgb("#204F57"))

  // TOOLS-202: use narrower table stroknes
  set table(stroke: 0.5pt + black)

  set outline(indent: 1em)

  show outline.entry.where(level: 1): it => {
    // XXX can this be done via .where()?
    if it.element.func() == heading {
      v(12pt, weak: true)
      strong(it)
    } else [
      #let location = it.element.location()
      #link(location)[
        #if figure-numbering [#it.body] else [#it.element.caption.body]]
      #box(width: 1fr, repeat[.])
      #link(location)[#it.page]
    ]
  }

  // why aren't figures breakable by default? blocks are
  show figure: set block(breakable: true)

  show figure.where(kind: table): set align(left)

  show figure.where(kind: table): set figure.caption(position: top)

  // XXX this should honor the pandoc titleDelim metadata variable
  show figure.caption: it => [
    *#if figure-numbering [#it.supplement
                           #it.counter.display(it.numbering):] #it.body*
  ]

  // XXX don't use bbf-raw-size here; it makes it too small; why?
  show raw.where(block: true): it => {
    set text(font: bbf-raw-font)
    it
  }

  /*
  // XXX this is disabled until can resolve the issues listed below
  // XXX is this still a problem?

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

  // set the document properties
  // XXX if authors is an array, we should pass an array
  set document(
    title: stringify(title),
    author: stringify(authors)
  )

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
      if loc.page() > 1 [
        #bbf-title #h(1fr) #bbf-number #bbf-issue #bbf-version]
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
