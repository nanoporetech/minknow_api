# Incompatible API Changes in MinKNOW API 6.0

The 6.0 release of of MinKNOW API has some breaking changes from the 5.x versions. The
breaking changes mostly revolve around LAMP and Dual barcode support being removed and
changing of the `guppy` nomenclature to generic `basecaller` style names

## Removed RPCs

### `manager.proto`

* `get_lamp_kit_info`: While not completely removed, LAMP support has been removed and
  calling into the API will just result in an empty message

## Changed Message Types

### `analysis_configuration.proto`

* `BarcodingConfiguration`: Fields `detect_mid_strand_barcodes`, `min_score`, `min_score_rear`,
  `min_score_mid` and `min_score_mask` have been removed. These fields are no longer supported
  with the switch from Guppy to Dorado

### `data.proto`

* `GetLiveReadsRequest.Action`: Field `number` has been removed. Reads that should be acted
  upon should be specified by their read id instead.

* `GetLiveReadsResponse.ReadData`: Field `number` has been removed. Responses now only
  provide the read id, as this is what should be used when actions need to be applied
  to the read

### `instance.proto`

* `GetVersionInfoResponse`: Removed fields `guppy_build_version` and `guppy_connected_version`
  Added fields `basecaller_build_version` and `basecaller_connected_version`.
  Adjustments made to move away from `guppy` related nomenclature to more generic names

### `manager.proto`

* `GetBarcodeKitInfoResponse.BarcodeKitInfo`: The field `is_dual` is deprecated and will
  always be `false`. Dual barcoding support has been removed in 6.0

### `statistics.proto`

* `AcquisitionOutputKey`: Fields `lamp_barcode_id` and `lamp_target_id` are deprecated and
  will be ignored. Lamp barcode support has been removed in 6.0
