from playwright.sync_api import sync_playwright
from PIL import Image
S='/tmp/claude-0/-home-claude/fe74ec05-d6da-5315-a401-9b31ca95aa3a/scratchpad/'
Image.new('RGB',(1600,1200),(90,120,150)).save(S+'foto.jpg')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':850}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    pg.route('**/*', lambda r: r.abort() if r.request.url.startswith('http') else r.continue_())
    pg.goto('file:///home/claude/infraapp/campo.html'); pg.wait_for_timeout(2500)
    pg.evaluate("""()=>{ usuarioCampo={id:'u',nome:'Teste',perfil:'Admin',obra:'o1'}; window._salvos=[]; fbSalvar=async(c,i)=>{_salvos.push([c,i])};
      dadosCampo.equipamentos=[{id:'e1',tag:'ESC-01',codModelo:'PC200',obra:'o1'}]; dadosCampo.modelos=[]; dadosCampo.tanques=[];
      document.querySelectorAll('.screen,.tela').forEach(s=>s.classList.remove('active'));
      const s=document.getElementById('fuel-equip'); s.innerHTML='<option value="e1">ESC-01</option>'; s.value='e1';
      document.getElementById('fuel-data').value='2026-11-02'; document.getElementById('fuel-hora').value='10:00'; document.getElementById('fuel-litros').value='300'; }""")
    pg.evaluate("salvarFuel()"); pg.wait_for_timeout(300); print('sem nada salvou?', pg.evaluate("_salvos.length"))
    pg.evaluate("document.getElementById('fuel-horimetro').value='1250'")
    pg.set_input_files('#fuel-btn-hor input', S+'foto.jpg'); pg.wait_for_timeout(800)
    pg.evaluate("salvarFuel()"); pg.wait_for_timeout(300); print('só horímetro salvou?', pg.evaluate("_salvos.length"))
    pg.set_input_files('#fuel-btn-total input', S+'foto.jpg'); pg.wait_for_timeout(800)
    pg.evaluate("salvarFuel()"); pg.wait_for_timeout(800)
    r=pg.evaluate("_salvos.map(([c,i])=>[c,i.id,i.tipo||'',i.fotoHor||'',i.fotoTotal||'',(i.img||'').length])"); print(r)
    print('fotos limpas', pg.evaluate("[_fuelFotos.hor,_fuelFotos.total]"), errs); b.close()
