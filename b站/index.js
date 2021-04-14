function durationTrans(a){
  var b = ""
  var h = parseInt(a/3600),
      m = parseInt(a%3600/60),
      s = parseInt(a%3600%60);
  if(h>0){
    h = h<10 ? '0'+h : h
    b += h+":"
  }
  m = m<10 ? '0'+m : m
  s = s<10 ? '0'+s : s
  b+=m+":"+s
  return b;
}
function compute(time){
    return durationTrans(time)
}