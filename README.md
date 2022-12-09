<h1 align ="center"> Marketplace distribuido</h1>

<h2 align ="center"> Alisson Rodrigues¹ ,  João Victor² </h2>
<h2 align ="center"> {alissonrdcsantos, jvitorsantdrade}@gmail.com </h2>

<p><i><strong> Resumo.</strong>  Este relatório descreve a implementação do sistema de Marketplaces distribuídos  , o sistema foi desenvolvido em linguagem de programação python utilizando os recursos disponibilizados, o framework Flask para uso do protocolo Rest na comunicação entre processos e na construção de uma API para consumo dos dados, visando atender à exigência de um sistema totalmente descentralizado foram usadas abordagens P2P bem como algoritmos de sincronização distribuídos. </i></p>

<h1>1 Introdução</h1>

<p>O avanço e popularização da internet contribuiu tanto para atividades no dia a dia das pessoas bem como nas atividades comerciais, empresariais e etc e compras pela internet tem ganhado maior ênfase, por isso os comerciantes visando não perder espaço para concorrentes em lojas digitais acabam se integrando no comercio eletrônico, uma das abordagens utilizadas é a utilização de marketplaces de grandes lojas para venda dos produtos da loja física em parceria com a digital.</p>

<p>Para integrar as lojas pequenas ao mercado digital e poder explorar mais benefícios e possíveis consumidores na web são criados os consórcios de marketplaces onde os produtos cadastrados em um marketplace participante do consorcio pode ser comprado a partir de qualquer marketplace.</p>

<p>Foi solicitado o desenvolvimento de um sistema web para uma rede de marketplaces de um consorcio, dentro das restrições está a utilização do protocolo Representational State Transfer (REST) para que a comunicação não seja bloqueada pelo firewall, a compra e consulta de qualquer item cadastrado em um marketplace pelos demais e uma arquitetura totalmente descentralizada para evitar pontos de falha e possibilitar certo grau de independência entre os marketplaces.</p>

<p>O restante deste relatório aborda a metodologia utilizada e foi organizado da seguinte forma. A seção 2 aborda a fundamentação teórica dos conceitos e tecnologias utilizadas na solução. A seção 3 apresenta a metodologia desenvolvida e os detalhes de implementação junto aos diagramas do sistema proposto. A seção 4 apresenta e discute os resultados obtidos. A seção 5 apresenta as conclusões sobre a solução projetada e conhecimentos adquiridos.</p>

<h1> 2 Fundamentação Téorica</h1>

<p>Dentro da construção de um sistema distribuído a escolha da arquitetura influencia o desenvolvimento do sistema por isso uma arquitetura adequada deve ser empregada, dos modelos presentes na construção de sistemas distribuídos optou-se por utilizar uma arquitetura descentralizada Peer to Peer( P2P ), na abordagem P2P cada end-point é um nó que pode atender requisições e fazer requisições a outro nó isto com uma comunicação de par a para com cada nó conectado ao outro, com o P2P é possível atender escalabilidade e descentralização das operações (Kurose,2006).</p>

<p>Uma interface de programação da aplicação( API ) define os protocolos para acesso e utilização dos dados de uma aplicação para serviços fora do sistema(RedHat,2020), projetando o sistema para vários end-points em servidores com firewalls para proteção o protocolo Representational State Transfer (Rest) é aplicado na construção de uma API Rest, dentro das especificações do Rest o protocolo utilizado é o HTTP e os dados são transferidos em formato JSON ou XML( DevMedia,2013 ).</p>

<p>A aplicação desenvolvida é construída como um sistema distribuído que pode ser caracterizado como conjunto de independente de computadores que se apresenta como um sistema único e coerente, no escopo de sistemas distribuídos encontramos aplicações centralizadas com um servidor central e aplicações descentralizadas, existem vários tipos de sistemas distribuídos que podem ser classificados quanto a aplicação e arquitetura (STEEN e TANENBAUM,2007).</p>

<p>Definir a ordem e prioridade de eventos é uma atividade comum na comunicação entre processos, para sistemas distribuídos em que os computadores possuem cada um seu próprio relógio não é possível garantir a sincronia com baseado em seus próprios relógios. Para sincronizar os processos em sistemas distribuídos algumas opções são apresentadas como relógios lógicos, relógios vetoriais, algoritmos de eleição, algoritmo de anel entre outros.</p>

<p>Os relógios lógicos de Lamport fornecem um meio de ordenar parcialmente eventos em sistemas distribuídos, por meio de duas regras o algoritmo é construído, o relógio é construindo como um escalar que a cada evento interno o relógio é incrementado por um valor determinado, a segunda regra é que em eventos entre processos o relógio é atualizado conforme o maior valor de relógio, um dos problemas do relógio logico é que ele não trata casos de eventos simultâneos.</p>

<p>Relógios vetoriais são construídos a partir dos relógios lógicos de Lamport e podem tratar violações de casualidade, o nome vetorial se dá pois o algoritmo expande os relógios lógicos escalares para um vetor em que cada posição é um relógio logico e o número de posições é o número total de processos, seguindo as duas regras do algoritmo de Lamport em todo evento interno o relógio interno é incrementado em 1 e em cada evento externo os relógios são comparados e atualizado pelo maior valor.</p>

<h1>3	Metodologia, Implementação e Testes</h3>

<p>No desenvolvimento da aplicação a primeira etapa abordada foi a escolha da arquitetura do sistema, baseado nas restrições de  um sistema totalmente descentralizado, a escalabilidade de novos marketplaces e inventario comum ao markletplaces foi escolhido utilizar uma arquitetura P2P.</p>

<p>As compras dos clientes deveriam ser realizadas por operações atômicas, uma compra acontece ou não, como produtos podem estar cadastrados em diversos marketplaces diferentes compras simultâneas e possíveis produtos ausentes tiveram de ser tratados, optou-se por deixar o marketplace em que um produto foi cadastrado como o responsável por atualizar os valores enquanto uma réplica apenas para leitura era enviada para os demais marketplaces, quando ocorrer uma compra o marketplace enviara um mensagem informando interesse para todos os outros e o marketplace responsável pelo produto ira determinar quem terá acesso ao produto.</p>

<p>Na construção da arquitetura P2P foi implementada classe peer, o peer fica responsável pela comunicação entre pares enviando as transações, mensagens no formato json com dados necessários, o peer também realiza um broadcast no locahost na faixa de portas de 10000 a 10099 para buscar os peers ativos.</p>

<p>Se tratando de um sistema distribuído não existe relógio global para todos processos por isso para sincronizar os processos foram utilizados relógios vetoriais, cada marketplace possui seu próprio relógio vetorial com um ID único que corresponde a sua posição no relógio, em sistemas reais com processos escalados dinamicamente os relógios seriam implementados como listas dinâmicas mas para o modelo de solução adotou-se um vetor simples para não aumentar a complexidade.</p>

<p>Os relógios são enviados juntos de cada transação para que possam ser atualizados. Quando uma compra tem de ser realizada os relógios lógicos são compartilhados entre todos pares até que se possa ordenar os eventos, o markteplace com o produto cadastrado na sua base de dados decide liberar o acesso a região critica para o processo correspondente a vez.</p>

<p>A API rest foi construída utilizando o framework Flask do pyhton3, a API fornece as rotas para acesso das funcionalidades especificadas para o produto dentre elas o cadastro de produtos, compra  de produtos, cadastro de marketplace e etc, usando o protocolo HTTP as requisições usam os métodos GET ou POST e retornam os dados no formato JSON.</p>

<h1> 4 Resultados</h1>

<p>Na validação do sistema foram executados testes que consistiram da execução dos módulos individuais e posteriormente de todo sistema em casos de testes estabelecidos.</p>

<p>A principal classe é marketplace.py. ela implementa o marketplace em que os produtos são cadastrados e podem ser comprados, outra classe implementada é a classe peer usada para comunicação P2P entre os pares por ultimo tem-se a classe vector que implementa o relógio vetorial.</p>

<p>Os marketplaces foram colocados em execução e individualmente testou-se as operações de cadastro e remoção de produtos confirmando sua funcionalidade. Ao testar o peer dentro do marketplace constatou-se que os peers podem comunicar-se entre si e podem se conectar no broadcast na rede.</p>

<p>A função de replicar as bases de dados de um marketplace para os outros funciona parcialmente visto que os peers podem enviar a transação com os dados replicados mas não de forma automática, é necessário realizar uma chamada a rota “transaction” para que seja iniciado.</p>

<p>Os relógios vetoriais são enviados junto da transação na troca de mensagens entretanto dentro do thread para ordenar os eventos e acesso a região critica dentro do marketplace a sincronização não ocorre e com isso as demais funcionalidades como a compra de produtos é comprometida pois a exclusão mutua acaba não sendo garantida.</p>

<h1> 5 Conclusão</h1>

<p>Dentro das considerações finais o problema não foi completamente solucionado visto que todas as especificações determinadas não foram atingidas mas algumas considerações acerca dos resultados finais podem ser apresentadas.</p>

<p>Pode-se implementar uma arquitetura totalmente descentralizada de um sistema distribuído com a utilização da abordagem P2P produzindo conhecimento acerca da construção, vantagens e desvantagens desta arquitetura, em especifico a construção do sistema distribuído contribuiu para uma nova visão no processo de construção de aplicações distribuídas. Com a restrição da comunicação via rest uma nova proposta de comunicação que se usa do protocolo teve de ser implementada para permitir a comunicação entre os marketplaces adequando assim o sistema as restrições políticas do cliente.</p>

<p>Por fim consideramos que com a correção e conclusão do algoritmo de sincronização dos relógios lógicos o sistema poderá ser finalizado e as demais funcionalidades dependentes da sincronização do relógio, individualmente os módulos operam corretamente e podem ser utilizados em outras aplicações. Concluindo este trabalho com uma possível proposta de solução para o problema de sincronização que é a reorganização do processo de trocas de mensagens de sincronização e do thread de ordenação do marketplace</p>

<h1>Referências</h1>

<p>ROSS, Keith W.; KUROSE, James F. Redes de Computadores e a Internet: Uma abordagem top-down. São, 2006.</p>
<p>RedHat. API REST. [2020]. Disponível em: <https://www.redhat.com/pt-br/topics/api/what-is-a-rest-api> Acesso em: 04 Dez. 2022.</p>
<p>DevMedia. Rest tutorial. [2013]. Disponível em: < https://www.devmedia.com.br/rest-tutorial/28912> Acesso em: 04 Dez. 2022.</p>
<p>STEEN, Maarten Van; TANENBAUM, Andrew S. Sistemas distribuídos: princípios e paradigmas. São Paulo, 2007.</p>
<p>Geekforgeeks. Lamport’s logical clock .[2022] . 	Disponível em: <https://www.geeksforgeeks.org/lamports-logical-clock/> Acesso em: 08 Dez. 2022.</p>

<h3>Para rodar o projeto você precisa dessas bibliotecas:<h3>


Python 3.9+ 
flask
uuid


Como iniciar:

python marketplace.py

este comando irá iniciar nossa função principal

Como configurar os marketplaces

foi testado apenas com o localhost como Host

as portas que devem ser colocadas quando for configurar o marketplace são: 10000, 10010, 10020, 10030, 10040, 10050, 10060, 10070, 10080, 10090

as demais portas estão alocadas para os possíveis "peers" que irão surgir

para se comunicar utilizando a API do marketplace escolhido, utilize a porta do mesmo.
