# closer-look

AI-assisted document extraction with confidence-based human review.

> Work in progress: final project (TCC).

## Idea

Companies still spend a lot of time manually checking documents. This project explores using an LLM to extract the key fields from those documents, estimating how confident the model is in each field, and sending only the uncertain ones to a person for review. Corrections can then feed back into the extraction.

The goal is to compare the process before and after: how much time, cost and error the review takes with and without the automation.

## Data

Only public data:

- **Invoices:** receipts from the Câmara dos Deputados parliamentary expense quota ([CEAP](https://dadosabertos.camara.leg.br/swagger/api.html?tab=staticfile)), which come with hand-entered fields to compare against.
- **Contracts:** public contracts from PNCP, through its [public API](https://pncp.gov.br/api/consulta/swagger-ui/index.html).

The focus is on digital PDFs, as they usually arrive at a company, not scans or photos.

## References

- [Beyond Accuracy: model confidence in KIE with conformal prediction](https://doi.org/10.1007/s10032-026-00572-y)
- [Beyond Logprobs: multi-signal confidence engine for document field extraction](https://arxiv.org/pdf/2606.24420)
- [ConfBench](https://huggingface.co/papers/2608.01792)
- [Can LLMs Express Their Uncertainty?](https://arxiv.org/abs/2306.13063)
- [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599)
