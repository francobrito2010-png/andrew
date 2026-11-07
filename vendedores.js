// Dados do stand e da equipa — APENAS informação pública verificada.
// Fontes: danielpinhoautomoveis.pt/empresa (equipa), danielpinho.standvirtual.com (cargos),
// elferspot.com (morada, telefone, fundação). Ver README → "Fontes dos dados".
// ⚠️ POR CONFIRMAR com o stand: telemóvel/email direto de cada vendedor
//    (por agora todos usam o contacto geral do stand).
window.STAND_INFO = {
  nome: 'Daniel Pinho',
  sub: 'Automóveis',
  logo: 'assets/marca/logo-branco.png',     // caminho a partir da raiz do site
  site: 'https://francobrito2010-png.github.io/andrew/', // onde fica alojado o perfil (o QR aponta aqui)
  web: 'www.danielpinhoautomoveis.pt',
  webUrl: 'https://www.danielpinhoautomoveis.pt/',
  morada: 'Rua Capitão Ramires 14, 1000-085 Lisboa',
  telefone: '+351 964 619 165',
  whatsapp: '351964619165',
  horario: '09:00–13:00 · 14:30–19:00'
};

window.VENDEDORES = [
  { id: 'daniel-pinho',  nome: 'Daniel Pinho',  cargo: 'Gestor Comercial', telefone: '', whatsapp: '', email: '', foto: '' },
  { id: 'nelson-costa',  nome: 'Nelson Costa',  cargo: 'Gestor Comercial', telefone: '', whatsapp: '', email: '', foto: '' },
  { id: 'joao-maciel',   nome: 'João Maciel',   cargo: 'Vendas',           telefone: '', whatsapp: '', email: '', foto: '' }
];
// Campos vazios → usa o contacto geral do stand. Quando houver o número direto, basta preenchê-lo.
