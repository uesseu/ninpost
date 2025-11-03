import json
import sys
from typing import Dict, Any
import json
from .css import css

header = f'''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <title>ninpost</title>
  <link rel="stylesheet" type="text/css" href="main.css">
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    {css}
  </style>
</head>
<body id="print-pdf">
'''

script = '''
  let memberNum = document.getElementsByClassName('members').length
  let mode = 'address'
  let locs = Array()

  function toNextAddress() {
    if (cur[book] != null && cur[book] < data[book].length - 1) cur[book]++;
    setAddress(book, cur[book])
  }

  function toPrevAddress() {
    if (cur[book]!== null && cur[book] > 0) cur[book] --;
    setAddress(book, cur[book])
  }

  function toNextBook() {
    if (book != null && book < data.length - 1) book ++;
    setAddress(book, cur[book])
  }

  function toPrevBook() {
    if (book !== null && book > 0) book --;
    setAddress(book, cur[book])
  }

  function setAddress(book, cur){
  console.log(book, cur)
    document.getElementById('familyName').innerText = data[book][cur]['familyName']
    document.getElementById('address').innerText = data[book][cur]['address']
    document.getElementById('post').innerText = data[book][cur]['post']
    for (let e in document.getElementsByClassName('members')){
      if (data[book][cur]['name'][e] === undefined) break
      document.getElementsByClassName('members')[e].innerText = data[book][cur]['name'][e]
      document.getElementsByClassName('titles')[e].innerText = data[book][cur]['title'][e]
    }
    document.getElementById('content').innerText = data[book][cur]['content']
    setContent()
    document.getElementById('draft').value = data[book][cur]['content'].replace("\\\\n", "\\n")
  }

  function enterContentMode(){
    mode = 'content'
    for (let n of ['familyName', 'myName', 'myPost', 'myAddress', 'address', 'post']) {
      document.getElementById(n).style.visibility = 'hidden'
    }
    for (let n of ['members', 'titles'])
      for (let e of document.getElementsByClassName(n))
        e.style.visibility = 'hidden'
    document.getElementById('content').style.visibility = 'visible'
    setContent()
    document.getElementById('draft').disabled = false
    document.getElementById('draft').focus()
  }

  function setContent(){
    let content = document.getElementById('content')
    let numEnter = 8 - document.getElementById('draft').value.split('\\n').length
    if (numEnter <= 0) numEnter = 0
    content.innerHTML = '<pre>' + document.getElementById('draft').value + '\\n'.repeat(numEnter) + '</pre>'
  }

  function enterAddressMode(){
    mode = 'address'
    for (let n of ['familyName', 'myName', 'myPost', 'myAddress', 'address', 'post']) {
      document.getElementById(n).style.visibility = 'visible'
    }
    for (let n of ['members', 'titles'])
      for (let e of document.getElementsByClassName(n))
        e.style.visibility = 'visible'
    document.getElementById('content').style.visibility = 'hidden'
    document.getElementById('draft').disabled = true
  }

  document.getElementById('draft').addEventListener('keyup', e=>{
    setContent()
  });

  document.addEventListener('keyup', e=>{
    if (mode==='address'){
      if (e.key === 'l') toNextAddress() 
      if (e.key === 'h') toPrevAddress() 
      if (e.key === 'j') toNextBook() 
      if (e.key === 'k') toPrevBook() 
      if (e.key === 'ArrowRight') toNextAddress() 
      if (e.key === 'ArrowLeft') toPrevAddress() 
      if (e.key === 'ArrowDown') toNextBook() 
      if (e.key === 'ArrowUp') toPrevBook() 
      if (e.key === 'i') enterContentMode() 
      if (e.key === 'p') window.print();
    } else {
      if (e.key === 'Escape') enterAddressMode() 
      if (e.key === 'p') window.print();
    }
  },
  false);

  document.addEventListener('click', e=>{
    let geometry = document.getElementById('center').getBoundingClientRect();
    if (mode === 'address'){
      if (e.clientY <= geometry.top) {
        window.print();
      } else if (e.clientX >= geometry.right) {
        toNextAddress();
      } else if (e.clientX <= geometry.left) {
        toPrevAddress();
      } else if (e.clientY > geometry.top && e.clientY < geometry.bottom) {
        enterContentMode()
      }
    } else if (mode === 'content') {
      if (e.clientY <= geometry.top) {
        window.print();
      } else if (e.clientY > geometry.top && e.clientY < geometry.bottom) {
        enterAddressMode()
      }
    }
  }, false);

  function setupView(){
    let style = document.getElementById('familyName').style
    style.left = `calc(${5.5 + memberNum * 0.2}cm - var(--body-left))`
    let menlen = 0
    for (const e of document.getElementsByClassName('members')) {
      if (e.innerText.length > menlen) menlen = e.innerText.length
    }
    for (let e = 0; e < memberNum; e++ ) {
      style = document.getElementsByClassName('titles')[e].style
      style.left = `calc(${5.5 - e + memberNum * 0.2}cm - var(--body-left))`
      style.top = `calc(${4.5 + document.getElementById('familyName').innerText.length + menlen}cm - var(--body-top))`
      style = document.getElementsByClassName('members')[e].style
      style.left = `calc(${5.5 - e + memberNum * 0.2}cm - var(--body-left))`
      style.top = `calc(${4 + document.getElementById('familyName').innerText.length}cm - var(--body-top))`
    }
  }
  setAddress(0, 0)
  setupView()
'''


def generate_html(
    data: list[dict[str, Any]], myself: dict[str, Any]
) -> str:
    json_data = json.dumps(data, ensure_ascii=True,)
    my_address = myself.get("address", "").replace('-', '|').replace('ー', '|')
    my_post = myself.get("myPost", "").replace('-', '|').replace('ー', '|')
    my_name = myself.get("myName", "").replace('-', '|').replace('ー', '|')
    lines = []
    lines.append('  <body id="print-pdf">')
    lines.append('    <link rel="stylesheet" type="text/css" href="main.css">')
    for n in ['center', 'post', 'address', 'familyName']:
        lines.append(f'    <span id="{n}"></span>')
    for n in range(5):
        lines.append(f'    <span class="members"></span>')
        lines.append(f'    <span class="titles"></span>')
    lines.append(f'    <span id="myAddress">{my_address}</span>')
    lines.append(f'    <span id="myPost">{my_post}</span>')
    lines.append(f'    <span id="myName">{my_name}</span>')
    lines.append(f'    <span id="content"></span>')
    lines.append(f'    <textarea id="draft" disabled></textarea>')
    return f'''{header}{'\n'.join(lines)}
    <script>
      const data = {json_data}
      let cur = 0
      cur = '0,'.repeat(data.length).split(',')
      cur.pop()
      let book = 0
      {script}
    </script>
   </body>
</html>'''
