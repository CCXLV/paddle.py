# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of the Paddle SDK
- Synchronous and asynchronous client implementations
- Support for Products API endpoints
- Comprehensive test suite
- Type hints throughout the codebase
- Retry mechanism for failed requests
- Environment configuration (Sandbox/Production)
- Error handling with custom exceptions

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## Planned API Endpoints

- [x] Products
  - [x] List
  - [x] Create
  - [x] Get
  - [x] Update

- [x] Prices
  - [x] List
  - [x] Create
  - [x] Get
  - [x] Update

- [ ] Discounts
  - [ ] List
  - [ ] Create
  - [ ] Get
  - [ ] Update
  
- [x] Customers
  - [x] List
  - [x] Create
  - [x] Get
  - [x] Update
  - [x] List credit balances
  - [x] Generate auth token

- [ ] Addresses
  - [ ] List
  - [ ] Create
  - [ ] Get
  - [ ] Update

- [ ] Businesses
  - [ ] List
  - [ ] Create
  - [ ] Get
  - [ ] Update

- [ ] Payment methods
  - [ ] List
  - [ ] Get
  - [ ] Delete

- [x] Customer portal sessions
  - [x] Create

- [ ] Transactions
  - [ ] List
  - [ ] Create
  - [ ] Get
  - [ ] Update
  - [ ] Preview
  - [ ] Get PDF Invoice
  - [ ] Revise

- [ ] Subscriptions
  - [x] List
  - [x] Get
  - [x] Preview
  - [x] Update
  - [ ] Get transaction to update payment method
  - [ ] Preview charge
  - [ ] Charge
  - [ ] Activate
  - [ ] Pause
  - [ ] Resume
  - [x] Cancel

- [ ] Adjustments
  - [ ] List
  - [ ] Create
  - [ ] PDF Credit note

- [ ] Pricing preview
  - [ ] Preview prices

- [ ] Reports
  - [ ] List
  - [ ] Create
  - [ ] Get
  - [ ] Get CSV

- [ ] Event types
  - [ ] List

- [ ] Events
  - [ ] List

- [ ] Notification settings
  - [ ] List
  - [ ] Create
  - [ ] Get
  - [ ] Update
  - [ ] Delete

- [ ] Notifications
  - [ ] List
  - [ ] Get
  - [ ] Replay

- [ ] Notification logs
  - [ ] List

- [ ] Simulation types
  - [ ] List

- [ ] Simulations
  - [ ] List
  - [ ] Create
  - [ ] Get
  - [ ] Update

- [ ] Simulation runs
  - [ ] List
  - [ ] Create
  - [ ] Get

- [ ] Simulation run events
  - [ ] List
  - [ ] Get
  - [ ] Replay