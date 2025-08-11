import json
import sys
from typing import Dict, Any

header = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <title>4.html</title>
  <link rel="stylesheet" type="text/css" href="main.css">
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    /* Minimal styling if main.css is unavailable */
    body { font-family: Arial, sans-serif; padding: 16px; }
    .row { display: block; margin: 4px 0; }
  </style>
</head>
<body id="print-pdf">
'''

script = '''
    (function(){
      let memberNum = document.getElementsByClassName('members').length
      let mode = 'address'

      function currentFileNumber() {
        const m = location.pathname.match(/(\\d+)\\.html$/);
        if (m) return parseInt(m[1], 10);
        return null;
      }
      
      function directoryPath() {
        const path = location.pathname;
        const idx = path.lastIndexOf('/');
        if (idx >= 0 && idx < letterNum) return path.substring(0, idx + 1);
        return '';
      }
      
      function navigateTo(num) {
        location.href = directoryPath() + num + ".html";
      }
      
      function navigateToNext() {
        const cur = currentFileNumber();
        if (cur != null && cur < letterNum - 1) navigateTo(cur + 1);
      }
      
      function navigateToPrev() {
        const cur = currentFileNumber();
        if (cur !== null && cur > 0) navigateTo(cur - 1);
      }

      function enterContentMode(){
        mode = 'content'
        document.getElementById('familyName').style.visibility = 'hidden'
        document.getElementById('myName').style.visibility = 'hidden'
        document.getElementById('myPost').style.visibility = 'hidden'
        document.getElementById('myAddress').style.visibility = 'hidden'
        document.getElementById('address').style.visibility = 'hidden'
        document.getElementById('post').style.visibility = 'hidden'
        for (let e of document.getElementsByClassName('members'))
          e.style.visibility = 'hidden'
        for (let e of document.getElementsByClassName('titles'))
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
        document.getElementById('familyName').style.visibility = 'visible'
        document.getElementById('myName').style.visibility = 'visible'
        document.getElementById('myPost').style.visibility = 'visible'
        document.getElementById('myAddress').style.visibility = 'visible'
        document.getElementById('address').style.visibility = 'visible'
        document.getElementById('post').style.visibility = 'visible'
        for (let e of document.getElementsByClassName('members'))
          e.style.visibility = 'visible'
        for (let e of document.getElementsByClassName('titles'))
          e.style.visibility = 'visible'
        document.getElementById('content').style.visibility = 'hidden'
        document.getElementById('draft').disabled = true
      }
      
      document.getElementById('draft').addEventListener('keyup', e=>{
        setContent()
      });

      document.addEventListener('keyup', e=>{
        if (mode==='address'){
          if (e.key === 'l') navigateToNext() 
          if (e.key === 'h') navigateToPrev() 
          if (e.key === 'ArrowRight') navigateToNext() 
          if (e.key === 'ArrowLeft') navigateToPrev() 
          if (e.key === 'i') enterContentMode() 
          if (e.key === 'p') window.print();
        } else {
          if (e.key === 'Escape') enterAddressMode() 
          if (e.key === 'p') window.print();
        }
      }
      ,false);

      document.addEventListener('click', e=>{
        let geometry = document.getElementById('center').getBoundingClientRect();
        if (mode === 'address'){
          if (e.clientY <= geometry.top) {
            window.print();
          } else if (e.clientX >= geometry.right) {
            navigateToNext();
          } else if (e.clientX <= geometry.left) {
            navigateToPrev();
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
      
      let style = document.getElementById('familyName').style
      style.left = `calc(${5.5 + memberNum * 0.2}cm - var(--body-left))`
      let menlen = 0
      for (const e of document.getElementsByClassName('members')) {
        if (e.innerText.length > menlen) menlen = e.innerText.length
      }
      for (const e in document.getElementsByClassName('titles')) {
        style = document.getElementsByClassName('titles')[e].style
        style.left = `calc(${5.5 - e + memberNum * 0.2}cm - var(--body-left))`
        style.top = `calc(${4.5 + document.getElementById('familyName').innerText.length + menlen}cm - var(--body-top))`
        style = document.getElementsByClassName('members')[e].style
        style.left = `calc(${5.5 - e + memberNum * 0.2}cm - var(--body-left))`
        style.top = `calc(${4 + document.getElementById('familyName').innerText.length}cm - var(--body-top))`
      }
    })();
     </script>
   </body>
</html>
'''

def generate_html(data: Dict[str, Any], myself: Dict[str, Any], letterNum=1, key='') -> str:
    post = data.get("post", "")
    address = data.get("address", "").replace('-', '|').replace('ー', '|')
    family_name = data.get("familyName", "")
    names = data.get("name", [])
    titles = data.get("title", [])
    my_address = myself.get("address", "").replace('-', '|').replace('ー', '|')
    my_post = myself.get("myPost", "")
    my_name = myself.get("myName", "")
    draft = data.get("content", "").replace('\\n', '\n')
    if 'prompt' in data and data.get('prompt', '') != '' and key:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        draft = client.responses.create(model="gpt-5-nano", input=data['prompt']).output_text

    lines = []
    lines.append('  <body id="print-pdf">')
    lines.append('    <link rel="stylesheet" type="text/css" href="main.css">')
    lines.append(f'    <span id="center"></span>')
    lines.append(f'    <span id="post">{post}</span>')
    lines.append(f'    <span id="address">{address}</span></p>')
    lines.append(f'    <span id="familyName">{family_name}</span>')
    for name, title in zip(names, titles):
        lines.append(f'    <span class="members">{name}</span>')
        lines.append(f'    <span class="titles">{title}</span></p>')
    lines.append(f'    <span id="myAddress">{my_address}</span>')
    lines.append(f'    <span id="myPost">{my_post}</span>')
    lines.append(f'    <span id="myName">{my_name}</span></p>')
    lines.append(f'    <span id="content">{draft}</span>')
    lines.append(f'    <textarea id="draft" disabled>{draft}</textarea>')
    return f'''{header}{'\n'.join(lines)}<script>const letterNum = {letterNum};
    {script}'''
