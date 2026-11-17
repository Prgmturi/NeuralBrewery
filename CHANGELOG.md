# Changelog

## [0.1.1](https://github.com/Prgmturi/NeuralBrewery/compare/v0.1.0...v0.1.1) (2026-11-17)


### Features

* add the brewer's dashboard in Streamlit ([a66dd49](https://github.com/Prgmturi/NeuralBrewery/commit/a66dd49d75128058f2f3d709728307c479094287))
* add the brewer's dashboard in Streamlit ([9300e38](https://github.com/Prgmturi/NeuralBrewery/commit/9300e3827a88d11f5c527c6a22afa353c2b4589d))
* add the manuals of the components, named by their id in the manifest ([d7629c9](https://github.com/Prgmturi/NeuralBrewery/commit/d7629c95a2ba254c0b9f8b939698c3c6b1ffd8a4))
* add the manuals of the pump and the fermenter, and write the valve's ([18973db](https://github.com/Prgmturi/NeuralBrewery/commit/18973db5ef0e90437812d43afe237962f6190fc9))
* add the manuals of the pump and the fermenter, write the valve's, drop the downloader ([32c9ad2](https://github.com/Prgmturi/NeuralBrewery/commit/32c9ad2c15dde5a313cc42f42616bc8226da8557))
* add the rules of the queue of approvals ([57b528a](https://github.com/Prgmturi/NeuralBrewery/commit/57b528ad530ded53b41968a71082fa3ba156d638))
* add the settings of the plant and of the approvals ([76bc6ef](https://github.com/Prgmturi/NeuralBrewery/commit/76bc6ef10534f3fe7efe7d293b06cbeb017c1bcf))
* diagnose plant alarms with a first agent on Claude ([bf17449](https://github.com/Prgmturi/NeuralBrewery/commit/bf17449a106ece0a90f8f7573a6911e774652bd5))
* diagnose plant alarms with a first agent on Claude ([10f5a74](https://github.com/Prgmturi/NeuralBrewery/commit/10f5a74eb451a1a7a90f4554d3e4fba47dc54cb4))
* execute a proposal on the plant only after the brewer approves it ([795d695](https://github.com/Prgmturi/NeuralBrewery/commit/795d6950de9e9c84d73b5bb477cd714860aeb532))
* extract the text of the manuals, one file per document ([506e201](https://github.com/Prgmturi/NeuralBrewery/commit/506e201496d8af6c50a1ca35f0a8c035257b3e70))
* judge the process with a watcher of fixed rules ([3863a1f](https://github.com/Prgmturi/NeuralBrewery/commit/3863a1ffe024dd64d037a09a055516dffae9ab0d))
* keep the events of the proposals in an append-only table ([85562a6](https://github.com/Prgmturi/NeuralBrewery/commit/85562a6096e5a9cf2f01f0ba21c630ea597331ab))
* let the agent propose reset, and run it on Gemini too ([a1fd297](https://github.com/Prgmturi/NeuralBrewery/commit/a1fd2977884391fb43bf567438ba7561a592a218))
* let the brewer propose a button with the approval token ([e73f7fd](https://github.com/Prgmturi/NeuralBrewery/commit/e73f7fd9f626fec1206ee9390a96b73ab96d53d4))
* let the plant agent diagnose from the API and queue its proposal ([0ecd011](https://github.com/Prgmturi/NeuralBrewery/commit/0ecd0111ab2fc8d3492b0b45bbfc777abc1437de))
* let the plant agent propose reset once the cause gives no more signs ([5f157a0](https://github.com/Prgmturi/NeuralBrewery/commit/5f157a020ef6053ab2013943881a200d173e6855))
* let the plant agent read the brewer's decisions on its past proposals ([6944367](https://github.com/Prgmturi/NeuralBrewery/commit/6944367b4ee20b31bb5d4766ef79a03b72449aad))
* let the plant agent recall the brewer's decisions ([27b3d7a](https://github.com/Prgmturi/NeuralBrewery/commit/27b3d7ac308989895f15705e8e6f72cbd4809a3f))
* let the plant agent search the manuals of the components ([78e9ca8](https://github.com/Prgmturi/NeuralBrewery/commit/78e9ca836b7d1f36443654da24894860f8ae6bf5))
* let the plant agent search the manuals of the components, on by default ([3c2b98d](https://github.com/Prgmturi/NeuralBrewery/commit/3c2b98de1bac78faa1909fefb946a52f804b98be))
* run the brew program in the controller ([6778253](https://github.com/Prgmturi/NeuralBrewery/commit/6778253ae672e8a92f7fadd167748aa025470395))
* run the plant agent on Gemini too, chosen by AGENT_PROVIDER ([17a0a2e](https://github.com/Prgmturi/NeuralBrewery/commit/17a0a2e697c0136388552770a592f2605ed7f885))
* serve an MCP server in the API that reads and proposes ([24d0a9f](https://github.com/Prgmturi/NeuralBrewery/commit/24d0a9f08799035b039b0c7ea7f829d8a6c88231))
* serve the dashboard from compose, in an image of its own ([5b9a1f2](https://github.com/Prgmturi/NeuralBrewery/commit/5b9a1f29fa9b1e2915867c4afee2d661133af6ad))
* serve the plant in the API, and approve with the token ([a2096d1](https://github.com/Prgmturi/NeuralBrewery/commit/a2096d1f4342f6ad496ebeb7df1ee05110fd8bc3))
* simulate the plant and its brew program ([e389cbc](https://github.com/Prgmturi/NeuralBrewery/commit/e389cbc47b9d0060fd4f6dab8f4ac300b8ab8990))
* simulate the plant behind a controller ([4f8f3fc](https://github.com/Prgmturi/NeuralBrewery/commit/4f8f3fc78dbe88e3ccd29975c1e941874df0ef25))
* turn the manuals on by default in the stack ([52b93b4](https://github.com/Prgmturi/NeuralBrewery/commit/52b93b4898bc52669038424405d12ad696199c20))


### Bug Fixes

* **deps:** take zlib1g from trixie-security, and scan both images in CI ([fa71ad9](https://github.com/Prgmturi/NeuralBrewery/commit/fa71ad9625ae11bba7d37116dd5726d3c9edfcd6))
* draw the dashboard only when Streamlit runs it ([c1b730e](https://github.com/Prgmturi/NeuralBrewery/commit/c1b730ef559848ef3f53f3de8af0eb92eaeb02a4))
* give Keycloak five minutes for its first start in the development stack ([5e68aed](https://github.com/Prgmturi/NeuralBrewery/commit/5e68aed368b511097f57698ae5ed21db791d9c1c))
* publish Postgres and Keycloak of the development stack on 127.0.0.1 only ([3667220](https://github.com/Prgmturi/NeuralBrewery/commit/3667220e7ba925e63ce9adf302be0e694471dc1e))
* publish the API of the development stack on 127.0.0.1 only ([8752f4a](https://github.com/Prgmturi/NeuralBrewery/commit/8752f4ac092640ee0f120839d746ea31289b80da))
* read the parameter list of the V20 one parameter a row ([b0798e6](https://github.com/Prgmturi/NeuralBrewery/commit/b0798e6d73fc60f23ed86f05e633c6912fad0ce1))
* say on a latched alarm that it waits for reset ([7cca596](https://github.com/Prgmturi/NeuralBrewery/commit/7cca5967a43bacd19188d61e731307143ade8a9d))
* say on the dashboard which tokens the API counts ([548f86e](https://github.com/Prgmturi/NeuralBrewery/commit/548f86e339ad967504aeb23ee80c10a22a7b1dae))
* turn CI green: zlib1g in both images, scan the dashboard, close the dev ports ([891a4e7](https://github.com/Prgmturi/NeuralBrewery/commit/891a4e7525ac192510025bbe6b6acedc8d0dbd96))

## Changelog
