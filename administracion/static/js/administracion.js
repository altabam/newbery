var f = document.createElement("form");
document.body.appendChild(f);

f.action = "/administracion/realizarBackup/personas";
f.method  ='GET'
f.submit();
f.action = "/administracion/realizarBackup/socios";
f.method  ='GET'
f.submit();