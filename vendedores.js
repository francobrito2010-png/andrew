// Vendedores do stand — cada um tem o seu QR e o seu perfil em vendedor/?v=<id>
// ⚠️ DEMO: nomes, telefones e números inventados. Substituir pelos dados reais.
// Para adicionar um vendedor: copiar um bloco, mudar o "id" (sem espaços nem acentos)
// e pôr a foto em assets/vendedores/<id>.webp (opcional — sem foto mostra as iniciais).
window.STAND_INFO = {
  nome: 'Daniel Pinho',
  sub: 'Automóveis',
  site: 'https://francobrito2010-png.github.io/andrew/',
  morada: 'Morada a confirmar',          // DEMO
  horario: 'Seg–Sex 9h–19h · Sáb 9h–13h' // DEMO
};

window.VENDEDORES = [
  {
    id: 'joao-silva',
    nome: 'João Silva',
    cargo: 'Consultor Comercial Sénior',
    desde: 2012,            // ano em que começou a vender carros → calcula os anos de experiência
    vendidos: 640,          // carros entregues (aprox.)
    telefone: '+351 910 000 001',
    whatsapp: '351910000001',
    email: 'joao@danielpinho.pt',
    foto: '',               // ex.: '../assets/vendedores/joao-silva.webp'
    especialidade: 'Desportivos e premium',
    frase: 'Encontro-lhe o carro certo — e trato de tudo até à entrega.',
    carros: ['ferrari-458-spider-rosso', 'aston-martin-vantage-roadster', 'ferrari-458-spider-blu'],
    demo: true
  },
  {
    id: 'ana-costa',
    nome: 'Ana Costa',
    cargo: 'Consultora Comercial',
    desde: 2018,
    vendidos: 310,
    telefone: '+351 910 000 002',
    whatsapp: '351910000002',
    email: 'ana@danielpinho.pt',
    foto: '',
    especialidade: 'Financiamento e retoma',
    frase: 'Simplifico o financiamento para que só tenha de escolher a cor.',
    carros: ['concept-gt-arancio', 'ferrari-458-spider-giallo', 'concept-gt-grigio'],
    demo: true
  }
];
