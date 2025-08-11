css = '''
:root {
  --body-left: 0cm;
  --body-top: 0cm;
}
.body{
  left: -1cm;
  top: -1cm
}
#post{
  margin: auto auto;
  position: fixed;
  width: 4.8cm;
  left: calc(4.5cm - var(--body-left));
  top: calc(1.3cm - var(--body-top));
  align: center;
  text-align:center;
  font-size: 0.8cm;
  letter-spacing: 3mm;
}
#familyName{
  margin: auto auto;
  position: fixed;
  left: calc(5.5cm - var(--body-left));
  top: calc(3.5cm - var(--body-top));
  writing-mode: vertical-rl;
  text-orientation: upright;
  font-size: 1cm;
  line-height: 1cm;
}
.members{
  margin: auto auto;
  position: fixed;
  left: calc(5.5cm - var(--body-left));
  top: calc(3.5cm - var(--body-top));
  writing-mode: vertical-rl;
  text-orientation: upright;
  font-size: 1cm;
  line-height: 1cm;
}
.titles{
  margin: auto auto;
  position: fixed;
  left: calc(5.5cm - var(--body-left));
  top: calc(3.5cm - var(--body-top));
  writing-mode: vertical-rl;
  text-orientation: upright;
  font-size: 1cm;
  line-height: 1cm;
}
#address{
  margin: auto auto;
  position: fixed;
  left: calc(7cm - var(--body-left));
  top: calc(3cm - var(--body-top));
  height: 9.5cm;
  width: 2cm;
  font-size: 0.5cm;
  writing-mode: vertical-rl;
  text-orientation: upright;
}
#myAddress{
  margin: auto auto;
  position: fixed;
  left: calc(1cm - var(--body-left));
  top: calc(6cm - var(--body-top));
  height: 6.2cm;
  width: 2cm;
  font-size: 0.35cm;
  writing-mode: vertical-rl;
  text-orientation: upright;
}
#myName{
  margin: auto auto;
  position: fixed;
  left: calc(0cm - var(--body-left));
  top: calc(8.3cm - var(--body-top));
  height: 2.8cm;
  width: 2cm;
  font-size: 0.4cm;
  writing-mode: vertical-rl;
  text-orientation: upright;
}
#myPost{
  margin: auto auto;
  position: fixed;
  left: calc(0.8cm - var(--body-left));
  top: calc(12.5cm - var(--body-top));
  height: 0.5cm;
  width: 3cm;
  font-size: 0.35cm;
  text-orientation: upright;
  letter-spacing: 2mm;
}
#content {
  left: 0.5cm
  width: calc(9cm - var(--body-top));
  visibility: hidden;
  position: fixed;
  top: 1cm;
  -webkit-writing-mode: vertical-rl;
      -ms-writing-mode: tb-rl;
          writing-mode: vertical-rl;
  font-size: 0.8cm;
}
#center {
  display: hidden;
  position: fixed;
  left: calc(3cm - var(--body-left));
  top: calc(3cm - var(--body-top));
  height: 12.4cm;
  width: 4cm;
}
#draft {
  position: fixed;
  left: calc(0cm - var(--body-left));
  top: calc(15.4cm - var(--body-top));
  height: 6cm;
  width: 10cm;
}
'''

