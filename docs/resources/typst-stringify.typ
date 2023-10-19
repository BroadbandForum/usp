// copied from BBF PDF Template
// XXX can you use local packages on the server?

#let stringify(value, as_list: false) = {
  let comps = ()
  if type(value) == "none" {
    // ignore
  }
  else if type(value) == "array" {
    for (i, item) in value.enumerate() {
      // XXX should this add a separator? this one?
      if i > 0 {
        comps.push(" " + sym.plus.circle + " ")
      }
      comps += stringify(item, as_list: true)
    }
  }
  else if type(value) == "dictionary" {
    for (i, pair) in value.pairs().enumerate() {
      // XXX should this add a separator? this one?
      if i > 0 {
        comps.push(" " + sym.plus.circle + " ")
      }
      // XXX shouldn't ignore the key?
      let (key, val) = pair
      comps += stringify(val, as_list: true)
    }
  }
  else if type(value) != "content" {
    // XXX might need to check some more types
    comps.push(str(value))
  } else if repr(value.func()) in ("space", "linebreak", "parbreak") {
    // XXX using repr is rather naughty
    // XXX space and parbreak aren't documented?
    comps.push(" ")
  } else if value.has("text") {
    comps.push(value.text)
  } else if value.has("body") {
    comps += stringify(value.body, as_list: true)
  } else if value.has("children") {
    for child in value.children {
      comps += stringify(child, as_list: true)
    }
  } else {
    // XXX not yet handled
    comps.push("<!" + repr(value) + "!>")
  }

  if as_list {
    return comps    
  } else if comps.len() == 0 {
    // XXX joining an empty array returns none; is this a bug?
    return ""
  } else {
    return comps.join()
  }
}

// test
#let test_stringify(content) = {
  [#repr(content) -> #stringify(content) \ ]
}

= Test stringify

#for content in (
  none,
  1,
  "",
  "1 2 3",
  (),
  ((1,), (2, 3)),
  ([*a* b], [c]),
  (a: 1, b: 2)
){
  test_stringify(content)  
}