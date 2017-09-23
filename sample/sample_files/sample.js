/* global tr */

function dummy () {
  console.log(tr('Hello, I am a sample text !'))
}

function dummyWithParameters (param1, param2) {
  console.log(
    tr('I can also take parameters in my text like %%(param1) and %%(param2)', {
      param1: param1,
      param2: param2
    })
  )
}

dummy()
dummyWithParameters('foo', 'bar')
