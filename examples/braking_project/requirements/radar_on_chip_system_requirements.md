# Radar-on-Chip System Requirements

This document provides a baseline set of 50 system-level requirements for an automotive Radar-on-Chip system, assuming a 77–81 GHz FMCW radar SoC used for ADAS / automated driving functions.

## Assumptions

- Target application: automotive ADAS / automated driving radar
- Radar type: FMCW Radar-on-Chip
- Operating band: 76 GHz to 81 GHz
- Typical use cases: front radar, corner radar, parking radar, and short-range object detection
- Requirement level: system requirements, not detailed hardware/software design requirements

## Requirements

| ID | System Requirement |
|---|---|
| ROC-SYS-001 | The Radar-on-Chip shall operate in the automotive radar frequency band from 76 GHz to 81 GHz. |
| ROC-SYS-002 | The Radar-on-Chip shall support FMCW radar operation with configurable chirp start frequency, slope, duration, and repetition period. |
| ROC-SYS-003 | The Radar-on-Chip shall support a maximum RF bandwidth of at least 4 GHz for high-resolution ranging. |
| ROC-SYS-004 | The Radar-on-Chip shall detect objects at a minimum distance of 0.2 m under nominal operating conditions. |
| ROC-SYS-005 | The Radar-on-Chip shall detect passenger vehicle-sized objects at a distance of at least 150 m under nominal operating conditions. |
| ROC-SYS-006 | The Radar-on-Chip shall provide range resolution of ≤ 10 cm when configured for maximum RF bandwidth. |
| ROC-SYS-007 | The Radar-on-Chip shall provide object relative velocity measurement with an accuracy of ±0.2 m/s under nominal conditions. |
| ROC-SYS-008 | The Radar-on-Chip shall support measurement of object relative velocity in the range of at least -100 m/s to +100 m/s. |
| ROC-SYS-009 | The Radar-on-Chip shall provide angular estimation in azimuth using multiple receive channels. |
| ROC-SYS-010 | The Radar-on-Chip shall provide azimuth angular accuracy of ≤ ±1° for objects with sufficient signal-to-noise ratio. |
| ROC-SYS-011 | The Radar-on-Chip shall support elevation angle estimation when connected to an antenna array with elevation diversity. |
| ROC-SYS-012 | The Radar-on-Chip shall support at least 3 transmit channels and 4 receive channels. |
| ROC-SYS-013 | The Radar-on-Chip shall support MIMO operation using time-division multiplexing between transmit channels. |
| ROC-SYS-014 | The Radar-on-Chip shall provide configurable transmit output power per transmit channel. |
| ROC-SYS-015 | The Radar-on-Chip shall monitor transmit output power and report deviations outside configured limits. |
| ROC-SYS-016 | The Radar-on-Chip shall include integrated low-noise receiver front-end circuitry for each receive channel. |
| ROC-SYS-017 | The Radar-on-Chip shall provide analog-to-digital conversion for each receive channel with a minimum resolution of 12 bits. |
| ROC-SYS-018 | The Radar-on-Chip shall support a configurable ADC sampling rate sufficient to process the maximum configured chirp bandwidth. |
| ROC-SYS-019 | The Radar-on-Chip shall provide raw ADC sample output for external radar signal processing. |
| ROC-SYS-020 | The Radar-on-Chip shall provide an integrated signal-processing path for range FFT processing. |
| ROC-SYS-021 | The Radar-on-Chip shall provide an integrated signal-processing path for Doppler FFT processing. |
| ROC-SYS-022 | The Radar-on-Chip shall support generation of a radar detection list containing at least range, relative velocity, azimuth angle, signal strength, and timestamp. |
| ROC-SYS-023 | The Radar-on-Chip shall support generation of a radar point cloud containing at least range, velocity, angle, and intensity information. |
| ROC-SYS-024 | The Radar-on-Chip shall timestamp radar measurements with a resolution of ≤ 1 ms. |
| ROC-SYS-025 | The Radar-on-Chip shall support synchronization with an external system time source. |
| ROC-SYS-026 | The Radar-on-Chip shall support frame rates configurable from 10 Hz to 50 Hz. |
| ROC-SYS-027 | The Radar-on-Chip shall complete radar acquisition, processing, and output transmission within 100 ms for a 10 Hz operating mode. |
| ROC-SYS-028 | The Radar-on-Chip shall support SPI communication for configuration, control, and diagnostic access. |
| ROC-SYS-029 | The Radar-on-Chip shall support a high-speed data interface for radar data output. |
| ROC-SYS-030 | The Radar-on-Chip shall provide interrupt signaling to the host processor for frame completion, error events, and diagnostic events. |
| ROC-SYS-031 | The Radar-on-Chip shall support boot-time configuration loading from non-volatile memory or an external host processor. |
| ROC-SYS-032 | The Radar-on-Chip shall complete initialization and be ready for radar operation within 500 ms after power supply stabilization. |
| ROC-SYS-033 | The Radar-on-Chip shall provide a defined safe state in which RF transmission is disabled. |
| ROC-SYS-034 | The Radar-on-Chip shall enter the safe state upon detection of a safety-critical internal fault. |
| ROC-SYS-035 | The Radar-on-Chip shall support startup built-in self-tests for RF, ADC, memory, clock, and processing subsystems. |
| ROC-SYS-036 | The Radar-on-Chip shall support periodic runtime diagnostics for RF signal chain integrity. |
| ROC-SYS-037 | The Radar-on-Chip shall detect internal clock failures and report the fault to the host processor. |
| ROC-SYS-038 | The Radar-on-Chip shall detect memory corruption in safety-relevant memories using ECC or equivalent protection. |
| ROC-SYS-039 | The Radar-on-Chip shall report diagnostic fault status using a structured fault register accessible by the host processor. |
| ROC-SYS-040 | The Radar-on-Chip shall support fault reaction times of ≤ 100 ms for safety-critical faults. |
| ROC-SYS-041 | The Radar-on-Chip shall support over-temperature detection and report the condition before exceeding the specified maximum junction temperature. |
| ROC-SYS-042 | The Radar-on-Chip shall operate over an ambient temperature range of at least -40 °C to +105 °C. |
| ROC-SYS-043 | The Radar-on-Chip shall monitor supply voltage rails and report undervoltage or overvoltage conditions. |
| ROC-SYS-044 | The Radar-on-Chip shall support low-power operating modes with RF transmission disabled. |
| ROC-SYS-045 | The Radar-on-Chip shall limit average power consumption to ≤ 5 W under nominal operating configuration. |
| ROC-SYS-046 | The Radar-on-Chip shall support secure firmware boot using cryptographic authentication. |
| ROC-SYS-047 | The Radar-on-Chip shall reject unauthenticated firmware images during boot or firmware update. |
| ROC-SYS-048 | The Radar-on-Chip shall support secure access control for configuration and calibration data. |
| ROC-SYS-049 | The Radar-on-Chip shall store calibration data for RF channels, ADC channels, and temperature compensation parameters. |
| ROC-SYS-050 | The Radar-on-Chip shall provide production test access for RF, digital, memory, interface, and diagnostic functions without compromising operational security. |

## Notes for Project Tailoring

The numerical values in this baseline should be tailored according to the final radar use case, vehicle-level function, safety concept, antenna configuration, regulatory constraints, and target silicon capabilities.

Examples of tailoring dimensions:

- Front long-range radar
- Corner radar
- Parking radar
- In-cabin radar
- Short-range object detection
- ASIL allocation and safety goals
- Cybersecurity concept
- Host processor architecture
- Radar processing partitioning between SoC and external ECU
