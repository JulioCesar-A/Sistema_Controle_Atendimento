import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: false,
})
export class HomePage {

  constructor() {}

  conteudoControle : { passo : number, conteudoTitulo : String[] } = {
    passo : 0,
    conteudoTitulo : [
      "BOAS VINDAS",
      "VOCÊ É PRIORIDADE? (IDOSO, PCD, GESTANTE)",
      "QUAL SEU TIPO DE ATENDIMENTO?",
      "SENHA EMITIDA"
    ]
  }

  senhaEmitir : { tipo : String, numSequencia : number, dataEmissao : Date } = {
    tipo: "",
    numSequencia: 0,
    dataEmissao: new Date(),
  }

  senhaEmitirFormatada : String = "";

  senhaEmitidas : { tipo : String, numSequencia : number, dataEmissao : Date }[] = [];
  
  sairTelaInicial() {
    if (this.conteudoControle.passo == 0) {
      this.conteudoControle.passo = this.conteudoControle.passo + 1;
    }
    console.log(this.conteudoControle.passo);
  }

  definirTipoSenha( tipo : String ) {
    if (tipo == "SP") {
      this.senhaEmitir.tipo = "SP";
    }
    if (tipo == "SE" && this.senhaEmitir.tipo != "SP") {
      this.senhaEmitir.tipo = "SE";
    }
    if (tipo == "SG" && this.senhaEmitir.tipo != "SP") {
      this.senhaEmitir.tipo = "SG";
    }
    console.log(this.senhaEmitir.tipo);
    this.conteudoControle.passo = this.conteudoControle.passo + 1;
    this.verificarPasso();

  }

  verificarPasso() {
    if (this.conteudoControle.passo === 3) {
      this.senhaEmitir.numSequencia = this.senhaEmitidas.length + 1;
      this.senhaEmitir.dataEmissao = new Date();


      this.senhaEmitirFormatada = this.senhaEmitir.dataEmissao.getFullYear().toString().substring(2);


      let mes: number = this.senhaEmitir.dataEmissao.getUTCMonth() + 1; 
      if (this.senhaEmitir.dataEmissao.getUTCMonth() < 10) {
        this.senhaEmitirFormatada += "0" + mes.toString();
      }
      this.senhaEmitirFormatada += this.senhaEmitir.dataEmissao.getDate().toString() + "-" + this.senhaEmitir.tipo + this.senhaEmitir.numSequencia.toString().padStart(2, '0');

      this.senhaEmitidas.push(this.senhaEmitir);
      console.log(this.senhaEmitir.dataEmissao);




      setTimeout(() => {
        this.conteudoControle.passo = 0;
        this.senhaEmitir = {
          tipo: "",
          numSequencia: 0,
          dataEmissao: new Date(),
        };
        this.senhaEmitirFormatada = "";
      }, 60000); // 1 minuto em milissegundos

    }
  }
}
