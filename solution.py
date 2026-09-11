import csv, urllib.request
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
ROOT=Path(__file__).parent
URL='https://raw.githubusercontent.com/akiladesarrollo/tech_interview/main/'
def ensure(name):
 p=ROOT/name
 if not p.exists(): urllib.request.urlretrieve(URL+name,p)
 return p
def triage():
 rows=list(csv.DictReader(ensure('correos_clientes.csv').open(encoding='utf-8-sig'))); seen=set(); out=[]
 for r in rows:
  text=((r['asunto'] or '')+' '+(r['cuerpo'] or '')).lower(); key=(r['remitente'],r['asunto'],r['cuerpo'])
  client=r['remitente']; typ='Consulta'; urg='Media'; action='Validar información y responder'; owner='Servicio al cliente'
  if key in seen: client+=' (duplicado)'; action='No crear segunda entrada; vincular al caso original'; owner='Automatización / control'
  elif 'bancolombia' in text and 'extracto' in text: client='Bancolombia (notificación automática)'; action='Archivar; no requiere seguimiento'; owner='Automatización / control'
  elif any(x in text for x in ('inundado','acabados','no quedó','nadie me contesta')): typ='Incidencia'; urg='Alta'; action='Abrir caso y escalar para solución'; owner='Postventa / Construcción'
  elif any(x in text for x in ('reclamo','desistir','devolución')): typ='Reclamación'; urg='Alta'; action='Registrar caso y validar con Jurídica y cartera'; owner='Servicio al cliente / Jurídica'
  elif any(x in text for x in ('cotización','precios','áreas disponibles','información','alianza')): typ='Pedido'; action='Enviar información comercial y asignar seguimiento'; owner='Comercial'
  elif 'sin asunto' in text or 'lo que hablamos' in text: urg='Alta'; action='Solicitar contexto antes de responder'
  elif any(x in text for x in ('urgente','hoy','desembolso esta semana')): urg='Alta'; action='Validar instrucciones y responder hoy'; owner='Cartera / Servicio al cliente'
  elif any(x in text for x in ('gracias','ok, muchas')): action='Cerrar o asociar al hilo existente'; owner='Automatización / control'
  seen.add(key); out.append({'Fecha':r['fecha_recepcion'],'Cliente':client,'Tipo':typ,'Urgencia':urg,'Acción':action,'Responsable':owner})
 with (ROOT/'seguimiento_correos.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
 return len(out)
def dashboard():
 rows=list(csv.DictReader(ensure('apartamentos_akila.csv').open(encoding='utf-8-sig'))); sold=[r for r in rows if r['estado']=='Vendido']; types=Counter(r['tipo_apartamento'] for r in sold); weeks=Counter()
 for r in sold:
  d=date.fromisoformat(r['fecha_venta']); weeks[str(d-timedelta(days=d.weekday()))[:10]]+=1
 weekly=''.join('<tr><td>'+w+'</td><td>'+str(n)+'</td></tr>' for w,n in sorted(weeks.items())); bytype=''.join('<tr><td>'+t+'</td><td>'+str(n)+'</td><td>'+format(n/len(sold),'.1%')+'</td></tr>' for t,n in sorted(types.items()))
 html='''<!doctype html><meta charset="utf-8"><title>Akila Dashboard</title><style>body{font:16px system-ui;max-width:1000px;margin:30px auto;color:#172033}section{display:inline-block;vertical-align:top;margin:8px;padding:18px;border:1px solid #ddd;border-radius:12px}table{border-collapse:collapse}td,th{padding:7px 18px;border-bottom:1px solid #ddd}</style><h1>Dashboard comercial · Proyecto Akila</h1><section><b>Vendidos</b><h2>'''+str(len(sold))+'''</h2></section><section><b>Disponibles</b><h2>'''+str(sum(r['estado']=='Disponible' for r in rows))+'''</h2></section><section><b>Tipos de producto</b><h2>'''+str(len(set(r['tipo_apartamento'] for r in rows)))+'''</h2></section><h2>Tipos vendidos</h2><table><tr><th>Tipo</th><th>Unidades</th><th>%</th></tr>'''+bytype+'''</table><h2>Ventas por semana</h2><table><tr><th>Semana</th><th>Unidades</th></tr>'''+weekly+'''</table>'''
 (ROOT/'dashboard.html').write_text(html,encoding='utf-8'); return len(rows),len(sold),sum(r['estado']=='Disponible' for r in rows)
if __name__=='__main__': print('Ejercicio 1:',triage(),'correos; Ejercicio 2:',dashboard(),'registros')
