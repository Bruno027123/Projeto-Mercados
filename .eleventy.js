module.exports = function(eleventyConfig) {
    // Copia a pasta pdfs para o site gerado
    eleventyConfig.addPassthroughCopy("pdfs");
    eleventyConfig.addPassthroughCopy("style.css"); // Adiciona para copiar o CSS também

    // Configura o Eleventy para ler arquivos de Markdown e Nunjucks (para templates)
    // e enviar o site gerado para a pasta "_site"
    return {
        dir: {
            input: ".", // Onde o Eleventy vai procurar os arquivos fonte (sua pasta atual)
            includes: "_includes", // Onde os pedaços de HTML reutilizáveis ficam
            data: "_data", // Onde dados globais podem ficar (não usaremos agora)
            output: "docs" // Onde o site final será gerado
        },
        templateFormats: ["html", "njk", "md"], // Formatos de arquivo que o Eleventy vai processar
        htmlTemplateEngine: "njk", // Engine para arquivos HTML (Nunjucks é bom para looping)
        markdownTemplateEngine: "njk" // Engine para arquivos Markdown
    };
};