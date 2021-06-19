

taxa = 0.0001
cotacao = 100 / ((1 - taxa) ** (366/252))


taxaMetaSelic = 11.25 / 100
vnaCompra = 3229.577978
vnaProjetado = vnaCompra * ( (1 + taxaMetaSelic) ** (1/252) )
preco= vnaProjetado * cotacao/100

print("Cotação:", cotacao )
print("Preço:", preco)