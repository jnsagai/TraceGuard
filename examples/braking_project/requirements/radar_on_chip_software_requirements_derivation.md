# Radar-on-Chip Software Requirements Derivation

This document derives software requirements from the 50 baseline Radar-on-Chip system requirements.

## Scope

The derived software requirements cover software responsibilities typically allocated to:

- Radar device firmware
- Radar configuration and control software
- Radar signal processing software
- Host-side radar driver and middleware
- Diagnostic and safety-management software
- Secure boot, update, and access-control software

RF, analog, antenna, power, and silicon characteristics are not assumed to be implemented purely by software. Where the parent system requirement is primarily hardware-related, the derived software requirements focus on configuration, validation, monitoring, calibration, diagnostics, data handling, and fault reaction.

## Requirement ID Convention

Software requirements use the following convention:

`ROC-SWR-XXX-YY`

Where:

- `XXX` maps to the parent system requirement number.
- `YY` is a sequential derived software requirement number under that parent.

Example:

`ROC-SWR-002-03` is the third software requirement derived from `ROC-SYS-002`.

## Derived Software Requirement Count

Total derived software requirements: **201**

## Verification Method Abbreviations

| Abbreviation | Meaning |
|---|---|
| T | Test |
| A | Analysis |
| I | Inspection |
| R | Review |
| D | Demonstration |

## Traceable Software Requirements

## ROC-SYS-001

**Parent system requirement:** The Radar-on-Chip shall operate in the automotive radar frequency band from 76 GHz to 81 GHz.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-001-01 | SW configuration | The radar software shall provide regional frequency-band configuration parameters defining the allowed RF start frequency, stop frequency, and guard margins for the 76 GHz to 81 GHz automotive radar band. | T, I |
| ROC-SWR-001-02 | SW validation | The radar software shall reject any radar profile whose configured chirp frequency range exceeds the configured regional frequency-band limits. | T, R |
| ROC-SWR-001-03 | SW diagnostics | The radar software shall read back the active RF frequency configuration after profile activation and shall report a configuration fault if the readback does not match the requested profile within configured tolerance. | T, I |

## ROC-SYS-002

**Parent system requirement:** The Radar-on-Chip shall support FMCW radar operation with configurable chirp start frequency, slope, duration, and repetition period.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-002-01 | SW configuration | The radar software shall provide a configuration interface for chirp start frequency, chirp slope, chirp duration, chirp idle time, and chirp repetition period. | T, I |
| ROC-SWR-002-02 | SW validation | The radar software shall validate each FMCW chirp profile for parameter range, parameter consistency, and hardware-supported limits before applying it to the Radar-on-Chip. | T, R |
| ROC-SWR-002-03 | SW sequencing | The radar software shall configure FMCW chirp sequences according to the selected radar frame profile before RF transmission is enabled. | T, A |
| ROC-SWR-002-04 | SW reporting | The radar software shall expose the active FMCW profile identifier and active chirp parameters to the host application or diagnostic interface. | T, I |

## ROC-SYS-003

**Parent system requirement:** The Radar-on-Chip shall support a maximum RF bandwidth of at least 4 GHz for high-resolution ranging.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-003-01 | SW configuration | The radar software shall support radar profiles with an RF sweep bandwidth up to 4 GHz, subject to the configured regulatory and device capability limits. | T, I |
| ROC-SWR-003-02 | SW validation | The radar software shall compute the requested RF sweep bandwidth from chirp slope and chirp duration and shall reject profiles exceeding the configured maximum bandwidth. | T, R |
| ROC-SWR-003-03 | SW processing | The radar processing software shall derive the range-bin scaling from the configured RF bandwidth and shall associate the scaling with each processed radar frame. | T, A |
| ROC-SWR-003-04 | SW diagnostics | The radar software shall report a bandwidth-configuration fault if the activated RF bandwidth differs from the requested bandwidth beyond configured tolerance. | T, I |

## ROC-SYS-004

**Parent system requirement:** The Radar-on-Chip shall detect objects at a minimum distance of 0.2 m under nominal operating conditions.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-004-01 | SW processing | The radar processing software shall support range-bin generation and reporting for detections at distances of 0.2 m and above when the active radar profile provides the required near-range coverage. | T, A |
| ROC-SWR-004-02 | SW configuration | The radar software shall provide a near-range radar profile optimized for short minimum detection distance. | T, I |
| ROC-SWR-004-03 | SW filtering | The radar processing software shall apply configurable near-range leakage, coupling, and static-clutter mitigation before reporting near-range detections. | T, I |
| ROC-SWR-004-04 | SW quality | The radar processing software shall assign a detection-quality indicator to near-range detections to support downstream plausibility checks. | T, I |

## ROC-SYS-005

**Parent system requirement:** The Radar-on-Chip shall detect passenger vehicle-sized objects at a distance of at least 150 m under nominal operating conditions.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-005-01 | SW configuration | The radar software shall provide at least one long-range radar profile intended to support detection of passenger vehicle-sized objects up to 150 m under nominal operating conditions. | T, I |
| ROC-SWR-005-02 | SW processing | The radar processing software shall process range bins covering at least 150 m when the long-range radar profile is active. | T, A |
| ROC-SWR-005-03 | SW filtering | The radar processing software shall use configurable detection thresholds for long-range detections to balance false alarms and missed detections according to the selected use case. | T, I |
| ROC-SWR-005-04 | SW reporting | The radar processing software shall mark detections beyond the validated range of the active radar profile as invalid or out-of-specification. | T, I |

## ROC-SYS-006

**Parent system requirement:** The Radar-on-Chip shall provide range resolution of <= 10 cm when configured for maximum RF bandwidth.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-006-01 | SW calculation | The radar software shall calculate the theoretical range resolution of each configured radar profile based on the active RF bandwidth. | T, R |
| ROC-SWR-006-02 | SW validation | The radar software shall identify profiles capable of achieving range resolution <= 10 cm when configured with maximum RF bandwidth. | T, R |
| ROC-SWR-006-03 | SW processing | The radar processing software shall use range-bin scaling consistent with the calculated range resolution for each radar frame. | T, A |
| ROC-SWR-006-04 | SW reporting | The radar software shall expose the calculated range resolution of the active profile to the host application or diagnostic interface. | T, I |

## ROC-SYS-007

**Parent system requirement:** The Radar-on-Chip shall provide object relative velocity measurement with an accuracy of +/-0.2 m/s under nominal conditions.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-007-01 | SW processing | The radar processing software shall calculate relative velocity for detected objects using Doppler processing of coherent radar frames. | T, A |
| ROC-SWR-007-02 | SW compensation | The radar processing software shall compensate relative velocity estimates for configured timing parameters, chirp repetition interval, and Doppler-bin scaling. | T, I |
| ROC-SWR-007-03 | SW quality | The radar processing software shall provide a velocity-quality or confidence indicator for each reported object. | T, I |
| ROC-SWR-007-04 | SW diagnostics | The radar software shall report a velocity-measurement degraded status when frame timing, synchronization, or processing conditions can prevent the target +/-0.2 m/s accuracy from being achieved. | T, I |

## ROC-SYS-008

**Parent system requirement:** The Radar-on-Chip shall support measurement of object relative velocity in the range of at least -100 m/s to +100 m/s.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-008-01 | SW configuration | The radar software shall provide radar profiles whose Doppler configuration supports relative velocity measurement from at least -100 m/s to +100 m/s when used under the intended operating assumptions. | T, I |
| ROC-SWR-008-02 | SW processing | The radar processing software shall represent signed relative velocity values and preserve the direction of motion in the radar output interface. | T, A |
| ROC-SWR-008-03 | SW ambiguity | The radar processing software shall detect velocity ambiguity conditions and shall report an ambiguity indicator when unambiguous velocity estimation cannot be guaranteed. | T, I |
| ROC-SWR-008-04 | SW validation | The radar software shall reject radar profiles whose configured Doppler range is below the minimum required velocity range for the selected operating mode. | T, R |

## ROC-SYS-009

**Parent system requirement:** The Radar-on-Chip shall provide angular estimation in azimuth using multiple receive channels.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-009-01 | SW configuration | The radar software shall configure the active receive-channel set and antenna geometry required for azimuth angle estimation. | T, I |
| ROC-SWR-009-02 | SW processing | The radar processing software shall estimate azimuth angle using phase information from multiple receive channels or virtual receive channels. | T, A |
| ROC-SWR-009-03 | SW calibration | The radar processing software shall apply configured per-channel phase and amplitude calibration before azimuth estimation. | T, I |
| ROC-SWR-009-04 | SW reporting | The radar output interface shall include azimuth angle and azimuth validity information for each object or point where azimuth estimation is available. | T, I |

## ROC-SYS-010

**Parent system requirement:** The Radar-on-Chip shall provide azimuth angular accuracy of <= +/-1 deg for objects with sufficient signal-to-noise ratio.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-010-01 | SW calibration | The radar software shall apply antenna-array calibration data required to support azimuth angular accuracy targets. | T, I |
| ROC-SWR-010-02 | SW quality | The radar processing software shall compute an azimuth-quality indicator based on signal-to-noise ratio, channel validity, and estimation residuals. | T, I |
| ROC-SWR-010-03 | SW filtering | The radar processing software shall suppress or mark as degraded azimuth estimates when the configured signal-to-noise threshold for angular accuracy is not met. | T, I |
| ROC-SWR-010-04 | SW diagnostics | The radar software shall report degraded angular-estimation capability when one or more receive channels required for the selected angular mode are unavailable. | T, I |

## ROC-SYS-011

**Parent system requirement:** The Radar-on-Chip shall support elevation angle estimation when connected to an antenna array with elevation diversity.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-011-01 | SW configuration | The radar software shall support configuration of antenna arrays containing elevation diversity information. | T, I |
| ROC-SWR-011-02 | SW processing | The radar processing software shall estimate elevation angle when the active antenna configuration and radar profile support elevation processing. | T, A |
| ROC-SWR-011-03 | SW interface | The radar output interface shall include elevation angle, elevation validity, and elevation-quality fields when elevation estimation is enabled. | T, A |
| ROC-SWR-011-04 | SW compatibility | The radar software shall disable elevation reporting or mark elevation as unavailable when the active antenna configuration does not support elevation diversity. | T, I |

## ROC-SYS-012

**Parent system requirement:** The Radar-on-Chip shall support at least 3 transmit channels and 4 receive channels.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-012-01 | SW configuration | The radar software shall support configuration and control of at least 3 transmit channels and 4 receive channels. | T, I |
| ROC-SWR-012-02 | SW channel management | The radar software shall maintain an active-channel mask for transmit and receive channels and shall apply it consistently during profile activation. | T, I |
| ROC-SWR-012-03 | SW diagnostics | The radar software shall perform channel-availability checks before enabling radar operation and shall report unavailable configured channels. | T, I |
| ROC-SWR-012-04 | SW reporting | The radar software shall expose the active transmit-channel and receive-channel configuration to the host application or diagnostic interface. | T, I |

## ROC-SYS-013

**Parent system requirement:** The Radar-on-Chip shall support MIMO operation using time-division multiplexing between transmit channels.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-013-01 | SW sequencing | The radar software shall configure time-division multiplexed transmit sequences for MIMO operation. | T, A |
| ROC-SWR-013-02 | SW data handling | The radar processing software shall associate acquired samples with the corresponding transmit slot and receive channel during MIMO operation. | T, A |
| ROC-SWR-013-03 | SW processing | The radar processing software shall form the configured virtual antenna array from TDM-MIMO transmit and receive combinations. | T, A |
| ROC-SWR-013-04 | SW validation | The radar software shall validate that the configured TDM-MIMO sequence is compatible with frame timing, Doppler processing, and active-channel constraints. | T, R |

## ROC-SYS-014

**Parent system requirement:** The Radar-on-Chip shall provide configurable transmit output power per transmit channel.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-014-01 | SW configuration | The radar software shall provide a transmit-power configuration parameter for each transmit channel. | T, I |
| ROC-SWR-014-02 | SW validation | The radar software shall validate requested transmit-power settings against device capability, regulatory limits, and safety limits before activation. | T, R |
| ROC-SWR-014-03 | SW persistence | The radar software shall support storage and retrieval of approved transmit-power calibration parameters. | T, I |
| ROC-SWR-014-04 | SW reporting | The radar software shall expose the requested and active transmit-power setting for each transmit channel. | T, I |

## ROC-SYS-015

**Parent system requirement:** The Radar-on-Chip shall monitor transmit output power and report deviations outside configured limits.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-015-01 | SW monitoring | The radar software shall periodically acquire transmit-output-power monitor data for each active transmit channel when supported by the device. | T, A |
| ROC-SWR-015-02 | SW diagnostics | The radar software shall compare monitored transmit output power against configured upper and lower limits. | T, I |
| ROC-SWR-015-03 | SW fault handling | The radar software shall report a transmit-power fault when monitored output power remains outside configured limits for longer than the configured debounce time. | T, I |
| ROC-SWR-015-04 | SW reaction | The radar software shall execute the configured fault reaction for transmit-power faults, including RF transmission disablement when classified as safety-critical. | T, A |

## ROC-SYS-016

**Parent system requirement:** The Radar-on-Chip shall include integrated low-noise receiver front-end circuitry for each receive channel.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-016-01 | SW configuration | The radar software shall configure receiver front-end parameters, including gain, channel enablement, and analog front-end mode, according to the active radar profile. | T, I |
| ROC-SWR-016-02 | SW monitoring | The radar software shall monitor receiver saturation, clipping, or overload indicators when provided by the device. | T, A |
| ROC-SWR-016-03 | SW diagnostics | The radar software shall report receiver front-end degradation when monitored receiver conditions exceed configured limits. | T, I |
| ROC-SWR-016-04 | SW processing | The radar processing software shall use receiver-channel status information to exclude invalid channels from downstream signal processing when required. | T, A |

## ROC-SYS-017

**Parent system requirement:** The Radar-on-Chip shall provide analog-to-digital conversion for each receive channel with a minimum resolution of 12 bits.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-017-01 | SW configuration | The radar software shall configure ADC resolution and data format according to the selected radar profile and supported device modes. | T, I |
| ROC-SWR-017-02 | SW validation | The radar software shall reject profiles that require ADC resolution below the minimum 12-bit requirement or an unsupported ADC data format. | T, R |
| ROC-SWR-017-03 | SW data handling | The radar software shall preserve ADC sample alignment, sign representation, and channel ordering when transferring ADC samples to the processing chain or external interface. | T, A |
| ROC-SWR-017-04 | SW diagnostics | The radar software shall report ADC configuration or ADC data-format mismatch faults detected during startup or runtime checks. | T, I |

## ROC-SYS-018

**Parent system requirement:** The Radar-on-Chip shall support a configurable ADC sampling rate sufficient to process the maximum configured chirp bandwidth.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-018-01 | SW calculation | The radar software shall calculate the required ADC sampling rate for each chirp profile based on beat-frequency and maximum-range assumptions. | T, R |
| ROC-SWR-018-02 | SW configuration | The radar software shall configure the ADC sampling rate according to the selected radar profile before radar frame acquisition starts. | T, I |
| ROC-SWR-018-03 | SW validation | The radar software shall reject profiles whose required ADC sampling rate exceeds the supported device sampling rate or configured processing throughput. | T, R |
| ROC-SWR-018-04 | SW diagnostics | The radar software shall report an ADC timing fault when the actual sampling configuration differs from the requested profile. | T, I |

## ROC-SYS-019

**Parent system requirement:** The Radar-on-Chip shall provide raw ADC sample output for external radar signal processing.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-019-01 | SW interface | The radar software shall provide a raw ADC sample output mode for external radar signal processing. | T, A |
| ROC-SWR-019-02 | SW data format | The radar software shall define and apply a raw ADC data format containing at least frame identifier, chirp index, channel identifier, sample index, sample value, and timestamp or time reference. | T, I |
| ROC-SWR-019-03 | SW bandwidth | The radar software shall verify that the selected raw ADC output mode does not exceed the configured high-speed interface throughput. | T, I |
| ROC-SWR-019-04 | SW access control | The radar software shall restrict access to raw ADC output mode according to configured access-control policy. | T, I |

## ROC-SYS-020

**Parent system requirement:** The Radar-on-Chip shall provide an integrated signal-processing path for range FFT processing.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-020-01 | SW processing | The radar processing software shall perform range FFT processing on acquired ADC samples for each active receive or virtual channel. | T, A |
| ROC-SWR-020-02 | SW configuration | The radar processing software shall support configurable range FFT length, window function, and zero-padding parameters. | T, I |
| ROC-SWR-020-03 | SW data integrity | The radar processing software shall verify that the number of acquired samples matches the configured range FFT input size before processing. | T, I |
| ROC-SWR-020-04 | SW reporting | The radar processing software shall provide range-spectrum or range-bin output to downstream processing stages according to the configured processing mode. | T, I |

## ROC-SYS-021

**Parent system requirement:** The Radar-on-Chip shall provide an integrated signal-processing path for Doppler FFT processing.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-021-01 | SW processing | The radar processing software shall perform Doppler FFT processing over coherent chirp sequences for each processed range bin. | T, A |
| ROC-SWR-021-02 | SW configuration | The radar processing software shall support configurable Doppler FFT length, Doppler window function, and coherent processing interval. | T, I |
| ROC-SWR-021-03 | SW data integrity | The radar processing software shall verify that the number of chirps available for Doppler processing matches the active Doppler configuration. | T, I |
| ROC-SWR-021-04 | SW reporting | The radar processing software shall provide Doppler-bin output or velocity estimates to downstream detection and object-generation stages. | T, I |

## ROC-SYS-022

**Parent system requirement:** The Radar-on-Chip shall support generation of a radar detection list containing at least range, relative velocity, azimuth angle, signal strength, and timestamp.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-022-01 | SW object output | The radar processing software shall generate a radar detection list for each processed frame when object-list output mode is enabled. | T, I |
| ROC-SWR-022-02 | SW data fields | Each radar detection-list entry shall contain at least range, relative velocity, azimuth angle, signal strength, timestamp, and validity information. | T, I |
| ROC-SWR-022-03 | SW limits | The radar software shall enforce a configured maximum number of detection-list entries per frame and shall report truncation when detections exceed this limit. | T, I |
| ROC-SWR-022-04 | SW serialization | The radar software shall serialize the radar detection list according to the configured host-interface message format. | T, I |

## ROC-SYS-023

**Parent system requirement:** The Radar-on-Chip shall support generation of a radar point cloud containing at least range, velocity, angle, and intensity information.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-023-01 | SW point-cloud output | The radar processing software shall generate a radar point cloud for each processed frame when point-cloud output mode is enabled. | T, I |
| ROC-SWR-023-02 | SW data fields | Each radar point-cloud entry shall contain at least range, velocity, angle, intensity, timestamp or frame time reference, and validity information. | T, I |
| ROC-SWR-023-03 | SW filtering | The radar processing software shall apply configurable point-cloud filtering for noise, static clutter, and minimum signal quality. | T, I |
| ROC-SWR-023-04 | SW limits | The radar software shall enforce a configured maximum number of point-cloud entries per frame and shall report truncation when points exceed this limit. | T, I |

## ROC-SYS-024

**Parent system requirement:** The Radar-on-Chip shall timestamp radar measurements with a resolution of <= 1 ms.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-024-01 | SW time base | The radar software shall maintain or consume a time base capable of timestamping radar measurements with <= 1 ms resolution. | T, I |
| ROC-SWR-024-02 | SW timestamping | The radar software shall assign a timestamp to each radar frame at a defined measurement point, such as frame start, frame end, or output generation. | T, I |
| ROC-SWR-024-03 | SW consistency | The radar software shall include the timestamp reference definition in the radar output interface specification. | T, I |
| ROC-SWR-024-04 | SW rollover | The radar software shall handle timestamp rollover without producing non-monotonic frame timestamps within the configured rollover handling interval. | T, I |

## ROC-SYS-025

**Parent system requirement:** The Radar-on-Chip shall support synchronization with an external system time source.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-025-01 | SW synchronization | The radar software shall provide an interface to synchronize the radar time base with an external system time source. | T, A |
| ROC-SWR-025-02 | SW quality | The radar software shall maintain a time-synchronization status indicating synchronized, not synchronized, degraded, or lost synchronization. | T, I |
| ROC-SWR-025-03 | SW drift monitoring | The radar software shall monitor time-base drift against the external time source when synchronization information is available. | T, A |
| ROC-SWR-025-04 | SW reporting | The radar output interface shall include time-synchronization status or time-quality information with each radar frame. | T, I |

## ROC-SYS-026

**Parent system requirement:** The Radar-on-Chip shall support frame rates configurable from 10 Hz to 50 Hz.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-026-01 | SW configuration | The radar software shall support radar frame-rate configuration from 10 Hz to 50 Hz for supported radar profiles. | T, I |
| ROC-SWR-026-02 | SW scheduling | The radar software shall schedule radar acquisition, processing, and output transmission according to the configured frame rate. | T, I |
| ROC-SWR-026-03 | SW validation | The radar software shall reject frame-rate configurations that are incompatible with the selected chirp sequence, processing load, or output bandwidth. | T, R |
| ROC-SWR-026-04 | SW monitoring | The radar software shall monitor actual frame period and shall report a frame-rate fault when the measured frame period violates configured tolerance. | T, A |

## ROC-SYS-027

**Parent system requirement:** The Radar-on-Chip shall complete radar acquisition, processing, and output transmission within 100 ms for a 10 Hz operating mode.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-027-01 | SW timing | The radar software shall measure the end-to-end latency from radar acquisition start to completion of output transmission for each frame or configurable subset of frames. | T, A |
| ROC-SWR-027-02 | SW performance | The radar software shall support acquisition, processing, and output scheduling such that the latency budget for 10 Hz operation does not exceed 100 ms under the specified processing configuration. | T, I |
| ROC-SWR-027-03 | SW overload handling | The radar software shall detect processing or output overload conditions that can violate the 100 ms latency requirement. | T, I |
| ROC-SWR-027-04 | SW reporting | The radar software shall report latency violations with frame identifier, measured latency, and active radar profile identifier. | T, I |

## ROC-SYS-028

**Parent system requirement:** The Radar-on-Chip shall support SPI communication for configuration, control, and diagnostic access.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-028-01 | SW driver | The radar software shall provide an SPI driver interface for Radar-on-Chip configuration, control, and diagnostic register access. | T, A |
| ROC-SWR-028-02 | SW integrity | The radar SPI communication software shall support configured data-integrity mechanisms such as CRC, parity, readback, or sequence counters where supported by the device protocol. | T, I |
| ROC-SWR-028-03 | SW error handling | The radar SPI communication software shall retry failed SPI transactions according to the configured retry policy and shall report persistent communication faults. | T, I |
| ROC-SWR-028-04 | SW concurrency | The radar software shall serialize or protect concurrent SPI access to prevent inconsistent device configuration or diagnostic reads. | T, I |

## ROC-SYS-029

**Parent system requirement:** The Radar-on-Chip shall support a high-speed data interface for radar data output.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-029-01 | SW interface | The radar software shall support at least one high-speed data-output interface for radar raw data, point-cloud data, or detection-list data. | T, A |
| ROC-SWR-029-02 | SW throughput | The radar software shall calculate expected output bandwidth for the selected radar profile and output mode before activation. | T, I |
| ROC-SWR-029-03 | SW flow control | The radar software shall implement flow-control, buffering, or backpressure handling for the high-speed output interface. | T, I |
| ROC-SWR-029-04 | SW diagnostics | The radar software shall report high-speed interface errors, including overflow, underflow, data loss, timeout, or link-down conditions. | T, I |

## ROC-SYS-030

**Parent system requirement:** The Radar-on-Chip shall provide interrupt signaling to the host processor for frame completion, error events, and diagnostic events.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-030-01 | SW interrupt handling | The radar software shall provide interrupt-service handling for frame completion, error events, and diagnostic events from the Radar-on-Chip. | T, I |
| ROC-SWR-030-02 | SW event mapping | The radar software shall map each supported interrupt source to a defined software event or diagnostic event. | T, I |
| ROC-SWR-030-03 | SW timing | The radar software shall process safety-relevant interrupt events within the configured interrupt latency budget. | T, A |
| ROC-SWR-030-04 | SW diagnostics | The radar software shall detect and report interrupt storm, missed interrupt, or unexpected interrupt conditions when supported by the platform. | T, I |

## ROC-SYS-031

**Parent system requirement:** The Radar-on-Chip shall support boot-time configuration loading from non-volatile memory or an external host processor.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-031-01 | SW configuration loading | The radar software shall support boot-time loading of radar configuration from non-volatile memory or from an external host processor. | T, I |
| ROC-SWR-031-02 | SW integrity | The radar software shall verify the integrity and compatibility of boot-time configuration before applying it. | T, I |
| ROC-SWR-031-03 | SW fallback | The radar software shall use a configured fallback configuration or remain in safe state when boot-time configuration validation fails. | T, I |
| ROC-SWR-031-04 | SW reporting | The radar software shall report the source, version, and validation status of the active boot-time configuration. | T, I |

## ROC-SYS-032

**Parent system requirement:** The Radar-on-Chip shall complete initialization and be ready for radar operation within 500 ms after power supply stabilization.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-032-01 | SW startup | The radar software shall implement a startup state machine covering power stabilization, device communication readiness, configuration loading, self-test execution, and radar-ready indication. | T, A |
| ROC-SWR-032-02 | SW timing | The radar software shall measure initialization time from power-supply stabilization indication to radar-ready state. | T, A |
| ROC-SWR-032-03 | SW timeout | The radar software shall detect and report startup timeout when initialization cannot complete within 500 ms under the specified startup configuration. | T, I |
| ROC-SWR-032-04 | SW optimization | The radar software shall support configuration of startup self-test scope to meet the 500 ms readiness target while preserving required diagnostic coverage. | T, I |

## ROC-SYS-033

**Parent system requirement:** The Radar-on-Chip shall provide a defined safe state in which RF transmission is disabled.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-033-01 | SW safe state | The radar software shall define a safe state in which RF transmission is disabled and no new radar frame acquisition is initiated. | T, I |
| ROC-SWR-033-02 | SW control | The radar software shall provide a controlled transition to safe state from startup, normal operation, degraded operation, and fault handling states. | T, I |
| ROC-SWR-033-03 | SW confirmation | The radar software shall verify RF transmission disablement by device status readback when entering safe state, if such status is available. | T, I |
| ROC-SWR-033-04 | SW reporting | The radar software shall report the current operational state, including safe state, to the host application or diagnostic interface. | T, I |

## ROC-SYS-034

**Parent system requirement:** The Radar-on-Chip shall enter the safe state upon detection of a safety-critical internal fault.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-034-01 | SW fault classification | The radar software shall classify internal faults according to configured severity levels, including safety-critical faults requiring safe-state transition. | T, I |
| ROC-SWR-034-02 | SW reaction | The radar software shall initiate transition to safe state upon detection of a safety-critical internal fault. | T, A |
| ROC-SWR-034-03 | SW priority | The radar software shall prioritize safe-state transition over non-safety-related processing when a safety-critical internal fault is detected. | T, I |
| ROC-SWR-034-04 | SW logging | The radar software shall log the triggering fault identifier, timestamp, and active operating mode when entering safe state due to a safety-critical fault. | T, I |

## ROC-SYS-035

**Parent system requirement:** The Radar-on-Chip shall support startup built-in self-tests for RF, ADC, memory, clock, and processing subsystems.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-035-01 | SW BIST orchestration | The radar software shall execute startup built-in self-tests for RF, ADC, memory, clock, and processing subsystems according to the configured startup diagnostic sequence. | T, I |
| ROC-SWR-035-02 | SW result handling | The radar software shall collect, evaluate, and store startup self-test results before enabling normal radar operation. | T, I |
| ROC-SWR-035-03 | SW fault handling | The radar software shall prevent transition to normal radar operation when a safety-critical startup self-test fails. | T, I |
| ROC-SWR-035-04 | SW reporting | The radar software shall expose startup self-test results through the diagnostic interface. | T, I |

## ROC-SYS-036

**Parent system requirement:** The Radar-on-Chip shall support periodic runtime diagnostics for RF signal chain integrity.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-036-01 | SW runtime diagnostics | The radar software shall execute periodic runtime diagnostics for RF signal-chain integrity according to the configured diagnostic schedule. | T, I |
| ROC-SWR-036-02 | SW non-interference | The radar software shall schedule runtime RF diagnostics so that they do not invalidate normal radar measurements unless the affected frames are explicitly marked invalid or diagnostic. | T, I |
| ROC-SWR-036-03 | SW result handling | The radar software shall evaluate runtime RF diagnostic results against configured thresholds. | T, I |
| ROC-SWR-036-04 | SW reporting | The radar software shall report RF signal-chain degradation or diagnostic failure to the host application or diagnostic interface. | T, I |

## ROC-SYS-037

**Parent system requirement:** The Radar-on-Chip shall detect internal clock failures and report the fault to the host processor.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-037-01 | SW monitoring | The radar software shall monitor internal clock status indicators provided by the Radar-on-Chip. | T, A |
| ROC-SWR-037-02 | SW diagnostics | The radar software shall detect loss of clock, clock out-of-range, clock monitor failure, or clock synchronization fault when reported by the device. | T, I |
| ROC-SWR-037-03 | SW reaction | The radar software shall execute the configured fault reaction for clock failures, including safe-state transition when the fault is classified as safety-critical. | T, A |
| ROC-SWR-037-04 | SW reporting | The radar software shall report clock-failure diagnostic events with timestamp and active radar profile identifier. | T, I |

## ROC-SYS-038

**Parent system requirement:** The Radar-on-Chip shall detect memory corruption in safety-relevant memories using ECC or equivalent protection.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-038-01 | SW configuration | The radar software shall enable ECC or equivalent memory-protection mechanisms for safety-relevant memories where software configuration is required. | T, I |
| ROC-SWR-038-02 | SW monitoring | The radar software shall monitor correctable and uncorrectable memory-error indicators for safety-relevant memories. | T, A |
| ROC-SWR-038-03 | SW reaction | The radar software shall report correctable memory errors according to configured thresholds and shall trigger the configured safety reaction for uncorrectable memory errors. | T, A |
| ROC-SWR-038-04 | SW diagnostics | The radar software shall support startup or periodic tests of memory-protection mechanisms where supported by the device. | T, I |

## ROC-SYS-039

**Parent system requirement:** The Radar-on-Chip shall report diagnostic fault status using a structured fault register accessible by the host processor.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-039-01 | SW fault model | The radar software shall maintain a structured diagnostic fault model containing fault identifier, severity, occurrence status, debouncing status, timestamp, and reaction status. | T, I |
| ROC-SWR-039-02 | SW register access | The radar software shall provide host-accessible diagnostic fault registers or diagnostic messages representing the structured fault status. | T, I |
| ROC-SWR-039-03 | SW lifecycle | The radar software shall define clear, latch, and aging behavior for each diagnostic fault status. | T, I |
| ROC-SWR-039-04 | SW consistency | The radar software shall ensure that fault status reported through different software interfaces is consistent for the same diagnostic event. | T, I |

## ROC-SYS-040

**Parent system requirement:** The Radar-on-Chip shall support fault reaction times of <= 100 ms for safety-critical faults.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-040-01 | SW timing | The radar software shall measure or bound the time from detection of a safety-critical fault to execution of the configured fault reaction. | T, A |
| ROC-SWR-040-02 | SW reaction budget | The radar software shall complete software-controlled fault reactions for safety-critical faults within 100 ms unless the safety concept allocates a shorter reaction time. | T, A |
| ROC-SWR-040-03 | SW priority | The radar software shall execute safety-critical fault reactions with higher priority than non-safety-related radar processing and data output. | T, I |
| ROC-SWR-040-04 | SW verification support | The radar software shall provide diagnostic hooks, logs, or counters enabling verification of safety-critical fault reaction time. | T, I |

## ROC-SYS-041

**Parent system requirement:** The Radar-on-Chip shall support over-temperature detection and report the condition before exceeding the specified maximum junction temperature.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-041-01 | SW monitoring | The radar software shall periodically acquire junction-temperature or temperature-sensor information from the Radar-on-Chip when available. | T, A |
| ROC-SWR-041-02 | SW thresholds | The radar software shall compare monitored temperature against configured warning, derating, and shutdown thresholds. | T, I |
| ROC-SWR-041-03 | SW reaction | The radar software shall execute configured thermal reactions, including diagnostic reporting, frame-rate reduction, transmit-power reduction, or RF disablement. | T, A |
| ROC-SWR-041-04 | SW reporting | The radar software shall report over-temperature and thermal-derating status to the host application or diagnostic interface. | T, I |

## ROC-SYS-042

**Parent system requirement:** The Radar-on-Chip shall operate over an ambient temperature range of at least -40 °C to +105 °C.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-042-01 | SW compensation | The radar software shall apply temperature-compensation parameters for RF, ADC, and signal-processing calibration over the supported operating temperature range. | T, I |
| ROC-SWR-042-02 | SW monitoring | The radar software shall monitor whether measured temperature is within the configured valid operating range. | T, A |
| ROC-SWR-042-03 | SW degraded mode | The radar software shall enter a configured degraded mode or safe state when temperature is outside the valid operating range. | T, I |
| ROC-SWR-042-04 | SW reporting | The radar software shall include temperature-range status in diagnostic reporting. | T, I |

## ROC-SYS-043

**Parent system requirement:** The Radar-on-Chip shall monitor supply voltage rails and report undervoltage or overvoltage conditions.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-043-01 | SW monitoring | The radar software shall periodically acquire supply-voltage monitor information for configured voltage rails when available. | T, A |
| ROC-SWR-043-02 | SW thresholds | The radar software shall compare monitored voltage values against configured undervoltage and overvoltage thresholds. | T, I |
| ROC-SWR-043-03 | SW reaction | The radar software shall execute configured reactions to voltage faults, including RF transmission disablement when the voltage fault is safety-critical. | T, A |
| ROC-SWR-043-04 | SW reporting | The radar software shall report supply-voltage diagnostic events with voltage-rail identifier, fault type, and timestamp. | T, I |

## ROC-SYS-044

**Parent system requirement:** The Radar-on-Chip shall support low-power operating modes with RF transmission disabled.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-044-01 | SW power modes | The radar software shall provide software states for normal operation, low-power operation, sleep, wakeup, and safe state as applicable to the Radar-on-Chip. | T, I |
| ROC-SWR-044-02 | SW RF control | The radar software shall ensure RF transmission is disabled before entering any low-power mode requiring RF-off behavior. | T, I |
| ROC-SWR-044-03 | SW wakeup | The radar software shall support controlled wakeup from low-power mode to the configured startup or ready state. | T, I |
| ROC-SWR-044-04 | SW data retention | The radar software shall define which configuration, calibration, fault, and synchronization data are retained or reloaded across low-power mode transitions. | T, I |

## ROC-SYS-045

**Parent system requirement:** The Radar-on-Chip shall limit average power consumption to <= 5 W under nominal operating configuration.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-045-01 | SW power management | The radar software shall provide power-management controls for frame rate, transmit duty cycle, processing load, and interface activity when supported by the system design. | T, A |
| ROC-SWR-045-02 | SW monitoring | The radar software shall estimate or acquire power-consumption-related telemetry under the nominal operating configuration. | T, A |
| ROC-SWR-045-03 | SW validation | The radar software shall reject or flag radar profiles expected to exceed the configured average power budget for the selected operating mode. | T, R |
| ROC-SWR-045-04 | SW reaction | The radar software shall support configured power-reduction reactions such as frame-rate reduction, transmit-power reduction, or low-power transition. | T, A |

## ROC-SYS-046

**Parent system requirement:** The Radar-on-Chip shall support secure firmware boot using cryptographic authentication.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-046-01 | SW secure boot | The radar software shall authenticate firmware images using a cryptographic signature or message authentication mechanism before execution. | T, I |
| ROC-SWR-046-02 | SW trust anchor | The radar software shall use a protected trust anchor or equivalent immutable verification basis for secure firmware boot. | T, I |
| ROC-SWR-046-03 | SW version control | The radar software shall verify firmware version and anti-rollback metadata before accepting a firmware image when anti-rollback protection is configured. | T, I |
| ROC-SWR-046-04 | SW reporting | The radar software shall report secure-boot status to the host application or diagnostic interface without exposing cryptographic secrets. | T, I |

## ROC-SYS-047

**Parent system requirement:** The Radar-on-Chip shall reject unauthenticated firmware images during boot or firmware update.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-047-01 | SW rejection | The radar software shall prevent execution of firmware images that fail cryptographic authentication. | T, I |
| ROC-SWR-047-02 | SW update | The radar software update mechanism shall verify firmware authenticity and integrity before committing an update image. | T, I |
| ROC-SWR-047-03 | SW fallback | The radar software shall retain or restore a known-good firmware image when a firmware update image is rejected. | T, I |
| ROC-SWR-047-04 | SW fault handling | The radar software shall report unauthenticated firmware rejection as a security event and shall remain in safe state or recovery state as configured. | T, I |

## ROC-SYS-048

**Parent system requirement:** The Radar-on-Chip shall support secure access control for configuration and calibration data.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-048-01 | SW access control | The radar software shall enforce access control for configuration data, calibration data, diagnostic commands, production-test functions, and firmware-update functions. | T, I |
| ROC-SWR-048-02 | SW authorization | The radar software shall require successful authorization before allowing modification of safety-relevant or security-relevant configuration and calibration data. | T, I |
| ROC-SWR-048-03 | SW integrity | The radar software shall protect stored configuration and calibration data against unauthorized modification using integrity checks and controlled write procedures. | T, I |
| ROC-SWR-048-04 | SW audit | The radar software shall log security-relevant access attempts and modification attempts according to the configured security policy. | T, I |

## ROC-SYS-049

**Parent system requirement:** The Radar-on-Chip shall store calibration data for RF channels, ADC channels, and temperature compensation parameters.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-049-01 | SW storage | The radar software shall store calibration data for RF channels, ADC channels, and temperature compensation parameters in a defined non-volatile or host-managed storage format. | T, I |
| ROC-SWR-049-02 | SW integrity | The radar software shall verify calibration-data integrity and compatibility before applying calibration data. | T, I |
| ROC-SWR-049-03 | SW application | The radar software shall apply valid calibration data during startup and whenever a radar profile requiring calibration is activated. | T, I |
| ROC-SWR-049-04 | SW fallback | The radar software shall enter degraded mode or safe state when required calibration data are missing, invalid, incompatible, or outside their validity conditions. | T, I |
| ROC-SWR-049-05 | SW traceability | The radar software shall expose calibration-data version, validity status, and application status to the host application or diagnostic interface. | T, I |

## ROC-SYS-050

**Parent system requirement:** The Radar-on-Chip shall provide production test access for RF, digital, memory, interface, and diagnostic functions without compromising operational security.

| Software Requirement ID | Allocation Area | Derived Software Requirement | Suggested Verification |
|---|---|---|---|
| ROC-SWR-050-01 | SW production mode | The radar software shall provide a production-test mode for RF, digital, memory, interface, and diagnostic test access. | T, I |
| ROC-SWR-050-02 | SW separation | The radar software shall prevent production-test commands from being executed during normal operational mode unless explicitly permitted by the safety and security concept. | T, I |
| ROC-SWR-050-03 | SW access control | The radar software shall require authorized access before enabling production-test mode or production-test functions. | T, I |
| ROC-SWR-050-04 | SW protection | The radar software shall ensure production-test access cannot bypass secure boot, access control, calibration integrity, or safety-critical fault reactions. | T, I |
| ROC-SWR-050-05 | SW exit criteria | The radar software shall define and enforce controlled exit from production-test mode before normal radar operation is enabled. | T, I |

## Notes for Further Refinement

These software requirements are suitable as an initial software requirement baseline. Before project use, they should be refined according to:

- Final vehicle-level radar function
- ASIL and safety concept allocation
- Item definition and intended operating environment
- Radar front-end and antenna design
- Silicon safety manual and hardware-software interface
- Cybersecurity concept and threat analysis
- Diagnostic coverage targets
- Data interface protocol and host ECU architecture
- Regulatory region and RF compliance constraints
- Intended split between on-chip firmware, host software, and external radar processing

## Recommended Next Step

For ISO 26262 / ASPICE usage, the next recommended step is to classify each software requirement by:

- Safety relevance
- ASIL allocation
- Software component allocation
- Verification method
- Verification level
- Requirement type: functional, performance, interface, safety, diagnostic, cybersecurity, calibration, or configuration
- Trace links to architecture elements and test cases
