## Como usar Kubernetes

### Passo 1: Preparar o Dockerfile
Se já possui um Dockerfile para o seu app, vamos confirmar que ele está pronto. Aqui está um exemplo de um Dockerfile básico para um projeto Python, que será a base do seu container:

```Dockerfile
# Usa uma imagem base oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para dentro do container
COPY . .

# Expõe a porta onde sua aplicação rodará
EXPOSE 5001

# Comando para rodar a aplicação
CMD ["python3", "app.py"]  
```

Certifique-se de ajustar o `Dockerfile` de acordo com as particularidades do seu projeto.

### Passo 2: Instalar e Configurar o Kubernetes (local)
Para executar Kubernetes localmente, você pode usar **Minikube** ou **kind** (Kubernetes in Docker). Abaixo estão as instruções com o Minikube:

1. **Instale o Minikube**:
   - No Debian, execute:
     ```bash
     sudo apt-get update
     sudo apt-get install -y curl
     curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
     sudo dpkg -i minikube_latest_amd64.deb
     ```
   
2. **Instale o kubectl**:
   - O `kubectl` é a ferramenta de linha de comando para Kubernetes.
     ```bash
     sudo apt-get install -y kubectl
     ```

3. **Inicie o Minikube**:
   - Após a instalação, inicie o cluster:
     ```bash
     minikube start
     ```

4. **Verifique se o Kubernetes está rodando**:
   ```bash
   kubectl get nodes
   ```

### Passo 3: Criar uma Imagem Docker do Projeto
Agora, crie a imagem Docker para o seu projeto.

1. **Crie a imagem** (a partir do Dockerfile):
   ```bash
   docker build -t my-bot-image .
   ```

2. **Verifique a imagem criada**:
   ```bash
   docker images
   ```

### Passo 4: Configurar o Deployment e o Service do Kubernetes
Agora que temos a imagem Docker, vamos configurar os arquivos de manifesto para Kubernetes. Esses arquivos dizem ao Kubernetes como rodar e expor sua aplicação.

1. **Crie um arquivo de deployment** (`deployment.yaml`):
   Este arquivo define como o Kubernetes irá criar e gerenciar seus pods.

   ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: house-deployment
    spec:
    replicas: 2
    selector:
        matchLabels:
        app: house
    template:
        metadata:
        labels:
            app: house
        spec:
        containers:
        - name: house-container
            image: juanvieira/house:latest
            ports:
            - containerPort: 5001
            resources:
            requests:
                memory: "256Mi"
                cpu: "500m"
            limits:
                memory: "512Mi"
                cpu: "1"
   ```

2. **Crie um arquivo de service** (`service.yaml`):
   O Service expõe a aplicação para fora do cluster.

   ```yaml
    apiVersion: v1
    kind: Service
    metadata:
    name: house-service
    spec:
    type: NodePort
    selector:
        app: house
    ports:
        - protocol: TCP
        port: 5001
        targetPort: 5001
        nodePort: 30001

   ```

### Passo 5: Aplicar os Manifests no Cluster
Agora que você criou os arquivos `deployment.yaml` e `service.yaml`, aplique-os no cluster Kubernetes:

1. **Aplicar o Deployment**:
   ```bash
   kubectl apply -f deployment.yaml
   ```

2. **Aplicar o Service**:
   ```bash
   kubectl apply -f service.yaml
   ```

3. **Verificar os Pods rodando**:
   ```bash
   kubectl get pods
   ```

4. **Verificar o Service**:
   ```bash
   kubectl get service
   ```

### Passo 6: Acessar a Aplicação
Se tudo estiver correto, você pode acessar a aplicação pela porta exposta. No caso do Minikube:

1. **Obtenha o IP do Minikube**:
   ```bash
   minikube ip
   ```

2. **Acesse a aplicação**:
   No navegador, acesse:
   ```
   http://<MINIKUBE_IP>:30007
   ```

   Substitua `<MINIKUBE_IP>` pelo IP retornado pelo comando anterior.

### Passo 7: Escalar a Aplicação (Opcional)
Com Kubernetes, você pode escalar facilmente o número de réplicas da sua aplicação.

1. **Escalar o número de réplicas**:
   ```bash
   kubectl scale deployment bot-deployment --replicas=5
   ```

2. **Verificar os Pods**:
   ```bash
   kubectl get pods
   ```

### Passo 8: Monitorar e Depurar
Você pode usar o Kubernetes para monitorar e depurar sua aplicação:

1. **Verificar os logs**:
   ```bash
   kubectl logs <POD_NAME>
   ```

2. **Obter detalhes dos recursos**:
   ```bash
   kubectl describe pod <POD_NAME>
   ```

### Passo 9: Encerrar o Minikube
Quando terminar, pode encerrar o Minikube:

```bash
minikube stop
```

## Kubernetes e Escalonamento de deployments no contexto de Machine Learning

Escalar os **deployments** no Kubernetes em projetos de **Machine Learning (ML)** pode trazer vários benefícios, especialmente em relação ao desempenho, resiliência, e eficiência do treinamento e da inferência de modelos. Aqui estão os principais motivos pelos quais você pode querer escalar deployments de ML:

### 1. **Paralelização do Treinamento**
No treinamento de modelos de machine learning, escalar os Pods permite distribuir o trabalho em várias máquinas (nós). Isso pode reduzir o tempo necessário para treinar grandes modelos ou processar grandes volumes de dados.

- **Exemplo:** Modelos complexos de deep learning, como redes neurais profundas, podem ser treinados mais rapidamente ao dividir os dados entre vários nós e treinar os modelos em paralelo. Isso é comum em frameworks como TensorFlow, que suporta treinamento distribuído.

### 2. **Escalar Inferência para Alta Disponibilidade**
Uma vez que um modelo é treinado e colocado em produção para realizar **inferência** (predições), a escalabilidade é crucial para garantir que o serviço possa lidar com um grande volume de solicitações em tempo real. Mais Pods significam mais instâncias do modelo em execução, o que distribui a carga e evita sobrecarga em um único ponto.

- **Exemplo:** Em um sistema de recomendação de produtos, como os usados por plataformas de e-commerce, o modelo de machine learning precisa inferir recomendações em tempo real para milhões de usuários. Escalar os Pods que executam a inferência permite atender a esse grande volume de solicitações com baixa latência.

### 3. **Serviços de Inferência em Tempo Real**
Para sistemas que exigem **inferência em tempo real**, como chatbots, assistentes virtuais, ou sistemas de detecção de fraudes, escalar o deployment garante tempos de resposta rápidos, mesmo em momentos de pico de tráfego.

- **Exemplo:** Um chatbot alimentado por um modelo de linguagem precisa responder rapidamente a muitas solicitações simultâneas. Escalando os Pods que realizam a inferência do modelo, o Kubernetes pode garantir que o serviço continue respondendo rapidamente, sem atrasos.

### 4. **Balanceamento de Carga e Autoescalabilidade**
Ao escalar os Pods em Kubernetes, você também pode utilizar mecanismos de **balanceamento de carga** para distribuir as requisições de inferência entre várias réplicas do modelo. Além disso, com o **Horizontal Pod Autoscaler (HPA)**, o número de Pods pode aumentar ou diminuir automaticamente com base em métricas de uso, como CPU, memória ou mesmo o número de requisições por segundo.

- **Exemplo:** Um serviço de recomendação de filmes pode ter maior demanda durante feriados ou fins de semana. Com autoescalabilidade, o Kubernetes pode aumentar o número de réplicas do modelo de machine learning para lidar com o aumento de requisições e depois reduzir automaticamente quando a demanda diminuir.

### 5. **Aumentar a Resiliência e Tolerância a Falhas**
Escalar deployments também aumenta a **resiliência** da sua aplicação. Se um ou mais Pods falharem, outros continuarão em execução, mantendo o serviço disponível. Isso é especialmente importante em projetos de machine learning que requerem alta disponibilidade, como modelos usados em sistemas críticos (monitoramento de saúde, detecção de fraudes, etc.).

- **Exemplo:** Se um Pod que faz inferência de um modelo de diagnóstico médico falhar, outros Pods que estão replicando a mesma tarefa podem continuar fornecendo as respostas, garantindo a continuidade do serviço.

### 6. **Treinamento Distribuído com GPUs**
Se seu treinamento de machine learning requer uso intensivo de **GPUs**, como em tarefas de deep learning, Kubernetes pode ser configurado para escalar Pods que usam nós equipados com GPUs, otimizando o uso desses recursos caros. Isso permite treinar modelos maiores ou mais complexos de maneira eficiente, sem sobrecarregar uma única GPU.

- **Exemplo:** Você pode escalar os Pods que usam GPUs para treinar um modelo de visão computacional em várias GPUs ao mesmo tempo, reduzindo o tempo de treinamento significativamente.

### 7. **Pipeline de Machine Learning com Componentes Distribuídos**
No contexto de **MLOps**, os pipelines de machine learning são compostos por várias etapas, como coleta de dados, pré-processamento, treinamento, avaliação e implantação. Escalar cada componente do pipeline em diferentes Pods permite que várias partes do pipeline sejam executadas simultaneamente, melhorando a eficiência e o throughput.

- **Exemplo:** Durante a etapa de pré-processamento de dados para treinamento de um modelo, você pode escalar os Pods responsáveis por processar diferentes partes dos dados em paralelo, acelerando o pipeline como um todo.

### 8. **Experimentos de Modelos e Hyperparameter Tuning**
Em machine learning, muitas vezes você precisa testar diferentes configurações e hiperparâmetros para encontrar a melhor versão do seu modelo. Escalando os Pods, você pode realizar **vários experimentos em paralelo**, reduzindo o tempo necessário para encontrar a melhor configuração.

- **Exemplo:** Ao usar ferramentas como o **Kubeflow** ou o **Ray**, você pode escalar Pods para testar diferentes combinações de hiperparâmetros de um modelo em paralelo, em vez de testar uma configuração por vez.

### 9. **Batch Inferencing**
Para inferência em lotes (batch), onde grandes volumes de dados precisam ser processados de uma vez, escalar Pods ajuda a distribuir essa carga entre várias réplicas, reduzindo o tempo de processamento.

- **Exemplo:** Um sistema de marketing pode querer processar milhares de perfis de usuários para gerar recomendações personalizadas de uma vez. Escalando os Pods, você pode processar esses dados em paralelo.

### Em resumo:
Escalar deployments em Kubernetes no contexto de machine learning melhora o desempenho, a disponibilidade e a eficiência, tanto no treinamento quanto na inferência de modelos. Seja para suportar cargas de trabalho intensas, distribuir tarefas de treinamento, realizar inferências em tempo real ou aumentar a resiliência do sistema, o escalonamento é uma ferramenta essencial para garantir que seus projetos de ML sejam eficientes e escaláveis.


## Como deletar deployments, pods e service

Para apagar os **Pods** e **Services** no Kubernetes, você pode usar os seguintes comandos:

### 1. **Apagar Pods**
Pods são gerenciados por **Deployments** ou **ReplicaSets**, então se você apenas apagar o Pod, ele será recriado pelo controlador responsável. Se você deseja realmente apagar o Pod sem que ele seja recriado, você precisa apagar o Deployment ou ReplicaSet responsável.

Para apagar **um Pod específico**:
```bash
kubectl delete pod <pod-name>
```

Para listar os Pods e verificar seus nomes:
```bash
kubectl get pods
```

### 2. **Apagar o Deployment (que controla os Pods)**
Se você deseja apagar todos os Pods associados a um Deployment, você pode apagar o Deployment diretamente:

```bash
kubectl delete deployment <deployment-name>
```

Para listar os Deployments:
```bash
kubectl get deployments
```

### 3. **Apagar Services**
Para apagar **um Service** específico:

```bash
kubectl delete service <service-name>
```

Para listar os Services:
```bash
kubectl get services
```

### Exemplo:
Se você tiver um deployment chamado `houses-deployment` e um service chamado `houses-service`, você pode apagá-los com os comandos:
```bash
kubectl delete deployment houses-deployment
kubectl delete service houses-service
```

