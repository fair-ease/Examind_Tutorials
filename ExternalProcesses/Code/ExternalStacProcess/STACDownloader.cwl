cwlVersion: v1.0
class: CommandLineTool
requirements:
  DockerRequirement:
    dockerPull: "images.geomatys.com/stac-downloader:latest"
inputs:
  stac_url:
    type: string
    inputBinding:
      position: 1
outputs:
  downloaded_asset:
    type: File
    outputBinding:
      glob: "*"
