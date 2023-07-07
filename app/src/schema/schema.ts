/* eslint-disable */
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
  /**
   * The `DateTime` scalar type represents a DateTime
   * value as specified by
   * [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
   */
  DateTime: any;
  /**
   * The `GenericScalar` scalar type represents a generic
   * GraphQL scalar value that could be:
   * String, Boolean, Int, Float, List or Object.
   */
  GenericScalar: any;
  /**
   * Leverages the internal Python implmeentation of UUID (uuid.UUID) to provide native UUID objects
   * in fields, resolvers and input.
   */
  UUID: any;
  /**
   * Create scalar that ignores normal serialization/deserialization, since
   * that will be handled by the multipart request spec
   */
  Upload: any;
};

export type AnalyzeDatasetGroup = {
  __typename?: 'AnalyzeDatasetGroup';
  datasetGroup?: Maybe<DatasetGroupType>;
};

export type AnalyzeDatasetGroupInputType = {
  datasetGroupId: Scalars['UUID'];
};

export enum AttrTypeType {
  Address = 'address',
  Area = 'area',
  Blank = 'blank',
  Contact = 'contact',
  Coordinate = 'coordinate',
  CountOfPeople = 'count_of_people',
  Date = 'date',
  Datetime = 'datetime',
  Event = 'event',
  FacilityName = 'facility_name',
  Length = 'length',
  Location = 'location',
  ModelNumber = 'model_number',
  Organization = 'organization',
  Person = 'person',
  Price = 'price',
  Quantity = 'quantity',
  Tel = 'tel',
  Term = 'term',
  Unknown = 'unknown',
  Weight = 'weight'
}

export type ChangeDatasetCurrentVersion = {
  __typename?: 'ChangeDatasetCurrentVersion';
  datasetGroup?: Maybe<DatasetGroupType>;
};

export type ConvertSuggestType = {
  __typename?: 'ConvertSuggestType';
  filterKey: Scalars['String'];
  filterParams: Scalars['String'];
  /** メッセージ */
  message?: Maybe<Scalars['String']>;
  /** インデックス */
  sourceIndex?: Maybe<Scalars['Int']>;
  /** 変換の短い文字列 */
  title?: Maybe<Scalars['String']>;
};

export type CreateConvertJob = {
  __typename?: 'CreateConvertJob';
  datasetConvertJob?: Maybe<DatasetConvertJobType>;
  status?: Maybe<JobStatusEnum>;
};

export type CreateConvertJobInputType = {
  datasetGroupId: Scalars['UUID'];
  filterKey: Scalars['String'];
  filterParams: Scalars['String'];
};

export type CreateConvertPreview = {
  __typename?: 'CreateConvertPreview';
  datasetPreview?: Maybe<DatasetPreviewType>;
  status?: Maybe<PreviewStatusEnum>;
};

export type CreateDatasetGroup = {
  __typename?: 'CreateDatasetGroup';
  datasetGroup?: Maybe<DatasetGroupType>;
};

export type CreateDatasetGroupInputType = {
  name: Scalars['String'];
  originalFile: Scalars['Upload'];
  source?: InputMaybe<DatasetSourceInputType>;
};

export type CreatePreviewInputType = {
  datasetGroupId: Scalars['UUID'];
  filterKey: Scalars['String'];
  filterParams: Scalars['String'];
};

export type CreateTemplateFromDatasetGroup = {
  __typename?: 'CreateTemplateFromDatasetGroup';
  datasetTemplate?: Maybe<DatasetTemplateType>;
};

export type CreateUser = {
  __typename?: 'CreateUser';
  user?: Maybe<UserType>;
};

export type CreateUserInputType = {
  email: Scalars['String'];
  name: Scalars['String'];
  password: Scalars['String'];
};

export enum DataTypeType {
  Boolean = 'boolean',
  Datetime = 'datetime',
  Float = 'float',
  Integer = 'integer',
  String = 'string',
  Unknown = 'unknown',
  Uri = 'uri'
}

export type DatasetAttrType = {
  __typename?: 'DatasetAttrType';
  attrType?: Maybe<AttrTypeType>;
  attrTypeName?: Maybe<Scalars['String']>;
  dataType?: Maybe<DataTypeType>;
  dataTypeName?: Maybe<Scalars['String']>;
  datasetId?: Maybe<Scalars['String']>;
  id?: Maybe<Scalars['UUID']>;
  index?: Maybe<Scalars['Int']>;
  name?: Maybe<Scalars['String']>;
  no?: Maybe<Scalars['Int']>;
  sampleValues?: Maybe<Array<Maybe<Scalars['String']>>>;
};

export type DatasetConvertJobType = {
  __typename?: 'DatasetConvertJobType';
  dataset?: Maybe<DatasetType>;
  errorMessages?: Maybe<Array<Maybe<Scalars['String']>>>;
  errors?: Maybe<Scalars['GenericScalar']>;
  filterKey?: Maybe<Scalars['String']>;
  hasError?: Maybe<Scalars['String']>;
  outputName?: Maybe<Scalars['String']>;
  result?: Maybe<Scalars['String']>;
  status?: Maybe<Scalars['String']>;
  taskId?: Maybe<Scalars['String']>;
};

export type DatasetCurrentVersionType = {
  __typename?: 'DatasetCurrentVersionType';
  id?: Maybe<Scalars['String']>;
};

/** An enumeration. */
export enum DatasetDeleteStatusEnum {
  Fail = 'FAIL',
  Success = 'SUCCESS'
}

export type DatasetGroupListType = {
  __typename?: 'DatasetGroupListType';
  datasetGroups?: Maybe<Array<Maybe<DatasetGroupType>>>;
  keyword?: Maybe<Scalars['String']>;
  page?: Maybe<Scalars['Int']>;
  pageSize?: Maybe<Scalars['Int']>;
  totalRecords?: Maybe<Scalars['Int']>;
};

export type DatasetGroupType = {
  __typename?: 'DatasetGroupType';
  createdAt?: Maybe<Scalars['DateTime']>;
  createdBy?: Maybe<Scalars['String']>;
  currentDataset?: Maybe<DatasetType>;
  currentVersion?: Maybe<DatasetCurrentVersionType>;
  datasets?: Maybe<Array<Maybe<DatasetType>>>;
  encoding?: Maybe<Scalars['String']>;
  id?: Maybe<Scalars['String']>;
  isOwner?: Maybe<Scalars['Boolean']>;
  name?: Maybe<Scalars['String']>;
  originalFile?: Maybe<Scalars['String']>;
  publicLevel?: Maybe<Scalars['Int']>;
  publicLevelName?: Maybe<Scalars['String']>;
  source?: Maybe<DatasetSourceType>;
  updatedAt?: Maybe<Scalars['DateTime']>;
};

export type DatasetPreviewType = {
  __typename?: 'DatasetPreviewType';
  dataset?: Maybe<DatasetType>;
  errorMessages?: Maybe<Array<Maybe<Scalars['String']>>>;
  errors?: Maybe<Scalars['GenericScalar']>;
  filterKey?: Maybe<Scalars['String']>;
  hasError?: Maybe<Scalars['Boolean']>;
  result?: Maybe<Scalars['String']>;
  status?: Maybe<Scalars['String']>;
  taskId?: Maybe<Scalars['String']>;
};

export type DatasetSourceInputType = {
  siteName?: InputMaybe<Scalars['String']>;
  siteUrl?: InputMaybe<Scalars['String']>;
};

export type DatasetSourceType = {
  __typename?: 'DatasetSourceType';
  id: Scalars['UUID'];
  siteName?: Maybe<Scalars['String']>;
  siteUrl?: Maybe<Scalars['String']>;
};

export type DatasetTemplateAttrType = {
  __typename?: 'DatasetTemplateAttrType';
  attrType?: Maybe<AttrTypeType>;
  attrTypeName?: Maybe<Scalars['String']>;
  dataType?: Maybe<DataTypeType>;
  dataTypeName?: Maybe<Scalars['String']>;
  desc?: Maybe<Scalars['String']>;
  id?: Maybe<Scalars['String']>;
  index?: Maybe<Scalars['Int']>;
  name?: Maybe<Scalars['String']>;
  no?: Maybe<Scalars['Int']>;
  sampleValues?: Maybe<Array<Maybe<Scalars['String']>>>;
};

export type DatasetTemplateType = {
  __typename?: 'DatasetTemplateType';
  attrs?: Maybe<Array<Maybe<DatasetTemplateAttrType>>>;
  desc?: Maybe<Scalars['String']>;
  id?: Maybe<Scalars['UUID']>;
  name?: Maybe<Scalars['String']>;
  sourceDataset?: Maybe<DatasetType>;
};

export type DatasetType = {
  __typename?: 'DatasetType';
  analyzedAt?: Maybe<Scalars['DateTime']>;
  analyzedStatus?: Maybe<Scalars['Int']>;
  annotateMessages?: Maybe<Array<Maybe<Scalars['String']>>>;
  attrNames?: Maybe<Array<Maybe<Scalars['String']>>>;
  attrs?: Maybe<Array<Maybe<DatasetAttrType>>>;
  createdAt?: Maybe<Scalars['DateTime']>;
  createdBy?: Maybe<Scalars['String']>;
  currentVersion?: Maybe<DatasetCurrentVersionType>;
  dataFile?: Maybe<Scalars['String']>;
  dataFileUrl?: Maybe<Scalars['String']>;
  datasetGroupId?: Maybe<Scalars['String']>;
  encoding?: Maybe<Scalars['String']>;
  fileSize?: Maybe<Scalars['Int']>;
  filterDetail?: Maybe<Scalars['String']>;
  filterJson?: Maybe<Scalars['String']>;
  hasAnnotates?: Maybe<Scalars['Boolean']>;
  id?: Maybe<Scalars['String']>;
  isAnalyzed?: Maybe<Scalars['Boolean']>;
  name?: Maybe<Scalars['String']>;
  numColumns?: Maybe<Scalars['Int']>;
  numRecords?: Maybe<Scalars['Int']>;
  updatedAt?: Maybe<Scalars['DateTime']>;
  version?: Maybe<Scalars['Int']>;
};

export type DeleteDataset = {
  __typename?: 'DeleteDataset';
  status?: Maybe<DatasetDeleteStatusEnum>;
};

export type DeleteDatasetGroup = {
  __typename?: 'DeleteDatasetGroup';
  status?: Maybe<StatusEnum>;
};

export type DeleteTemplate = {
  __typename?: 'DeleteTemplate';
  status?: Maybe<TemplateStatusEnum>;
};

export type EnumType = {
  __typename?: 'EnumType';
  name?: Maybe<Scalars['String']>;
  value?: Maybe<Scalars['String']>;
};

export type FilterType = {
  __typename?: 'FilterType';
  description?: Maybe<Scalars['String']>;
  helpText?: Maybe<Scalars['String']>;
  key?: Maybe<Scalars['String']>;
  name?: Maybe<Scalars['String']>;
  params?: Maybe<Array<Maybe<ParamType>>>;
};

/** An enumeration. */
export enum JobStatusEnum {
  Fail = 'FAIL',
  Success = 'SUCCESS'
}

export type Mutation = {
  __typename?: 'Mutation';
  analyzeDatasetGroup?: Maybe<AnalyzeDatasetGroup>;
  changeDatasetCurrentVersion?: Maybe<ChangeDatasetCurrentVersion>;
  createConvertJob?: Maybe<CreateConvertJob>;
  createConvertPreview?: Maybe<CreateConvertPreview>;
  createDatasetGroup?: Maybe<CreateDatasetGroup>;
  createTemplateFromDatasetGroup?: Maybe<CreateTemplateFromDatasetGroup>;
  createUser?: Maybe<CreateUser>;
  deleteDataset?: Maybe<DeleteDataset>;
  deleteDatasetGroup?: Maybe<DeleteDatasetGroup>;
  deleteTemplate?: Maybe<DeleteTemplate>;
  passwordReset?: Maybe<PasswordReset>;
  passwordResetRequest?: Maybe<PasswordResetRequest>;
  refreshToken?: Maybe<Refresh>;
  revokeToken?: Maybe<Revoke>;
  /** Obtain JSON Web Token mutation */
  tokenAuth?: Maybe<ObtainJsonWebToken>;
  updateDatasetAttr?: Maybe<UpdateDatasetAttr>;
  updateDatasetGroup?: Maybe<UpdateDatasetGroup>;
  updateTemplate?: Maybe<UpdateTemplate>;
  updateTemplateAttr?: Maybe<UpdateTemplateAttr>;
  updateUser?: Maybe<UpdateUser>;
  verifyToken?: Maybe<Verify>;
};


export type MutationAnalyzeDatasetGroupArgs = {
  input: AnalyzeDatasetGroupInputType;
};


export type MutationChangeDatasetCurrentVersionArgs = {
  datasetGroupId: Scalars['UUID'];
  version: Scalars['Int'];
};


export type MutationCreateConvertJobArgs = {
  input: CreateConvertJobInputType;
};


export type MutationCreateConvertPreviewArgs = {
  input: CreatePreviewInputType;
};


export type MutationCreateDatasetGroupArgs = {
  input: CreateDatasetGroupInputType;
};


export type MutationCreateTemplateFromDatasetGroupArgs = {
  datasetGroupId: Scalars['UUID'];
};


export type MutationCreateUserArgs = {
  input: CreateUserInputType;
};


export type MutationDeleteDatasetArgs = {
  datasetGroupId: Scalars['UUID'];
};


export type MutationDeleteDatasetGroupArgs = {
  datasetGroupId: Scalars['UUID'];
};


export type MutationDeleteTemplateArgs = {
  templateId: Scalars['UUID'];
};


export type MutationPasswordResetArgs = {
  password: Scalars['String'];
  passwordResetToken: Scalars['String'];
};


export type MutationPasswordResetRequestArgs = {
  email: Scalars['String'];
};


export type MutationRefreshTokenArgs = {
  refreshToken?: InputMaybe<Scalars['String']>;
};


export type MutationRevokeTokenArgs = {
  refreshToken?: InputMaybe<Scalars['String']>;
};


export type MutationTokenAuthArgs = {
  email: Scalars['String'];
  password: Scalars['String'];
};


export type MutationUpdateDatasetAttrArgs = {
  input: UpdateDatasetAttrInputType;
};


export type MutationUpdateDatasetGroupArgs = {
  input: UpdateDatasetGroupInputType;
};


export type MutationUpdateTemplateArgs = {
  input: UpdateTemplateInputType;
};


export type MutationUpdateTemplateAttrArgs = {
  input: UpdateTemplateAttrInputType;
};


export type MutationUpdateUserArgs = {
  input: UpdateUserInputType;
};


export type MutationVerifyTokenArgs = {
  token?: InputMaybe<Scalars['String']>;
};

/** Obtain JSON Web Token mutation */
export type ObtainJsonWebToken = {
  __typename?: 'ObtainJSONWebToken';
  payload: Scalars['GenericScalar'];
  refreshExpiresIn: Scalars['Int'];
  refreshToken: Scalars['String'];
  token: Scalars['String'];
};

export type ParamType = {
  __typename?: 'ParamType';
  arguments?: Maybe<Scalars['GenericScalar']>;
  defaultValue?: Maybe<Scalars['String']>;
  description?: Maybe<Scalars['String']>;
  group?: Maybe<Scalars['String']>;
  helpText?: Maybe<Scalars['String']>;
  label?: Maybe<Scalars['String']>;
  name?: Maybe<Scalars['String']>;
  required?: Maybe<Scalars['Boolean']>;
  type?: Maybe<Scalars['String']>;
};

export type PasswordReset = {
  __typename?: 'PasswordReset';
  user?: Maybe<UserType>;
};

export type PasswordResetRequest = {
  __typename?: 'PasswordResetRequest';
  user?: Maybe<UserType>;
};

/** An enumeration. */
export enum PreviewStatusEnum {
  Fail = 'FAIL',
  Success = 'SUCCESS'
}

export type Query = {
  __typename?: 'Query';
  attrTypes?: Maybe<Array<Maybe<EnumType>>>;
  /** 変換フィルターを検索します。 */
  convertorFilters?: Maybe<Array<Maybe<FilterType>>>;
  convertorsDatasetGroupAttrs?: Maybe<Array<Maybe<DatasetAttrType>>>;
  /** ??? */
  convertorsDatasetGroups?: Maybe<Array<Maybe<DatasetGroupType>>>;
  dataTypes?: Maybe<Array<Maybe<EnumType>>>;
  dataset?: Maybe<DatasetType>;
  datasetAttrs?: Maybe<Array<Maybe<DatasetAttrType>>>;
  datasetGroup?: Maybe<DatasetGroupType>;
  datasetGroupAttrs?: Maybe<Array<Maybe<DatasetAttrType>>>;
  datasetGroups?: Maybe<DatasetGroupListType>;
  ownDatasetGroups?: Maybe<DatasetGroupListType>;
  ownTemplates?: Maybe<Array<Maybe<DatasetTemplateType>>>;
  ownUser?: Maybe<UserType>;
  similarDatasets?: Maybe<Array<Maybe<SimilarDatasetType>>>;
  /** データセットグループ向けの変換のサジェストを行います。 */
  suggestByDatasetGroup?: Maybe<SuggestDatasetGroupType>;
  /** テンプレート向けの変換のサジェストを行います。 */
  suggestByDatasetTemplate?: Maybe<SuggestDatasetTemplateType>;
  templateAttrs?: Maybe<Array<Maybe<DatasetTemplateAttrType>>>;
  templates?: Maybe<Array<Maybe<DatasetTemplateType>>>;
};


export type QueryConvertorFiltersArgs = {
  datasetAttrIds?: InputMaybe<Array<InputMaybe<Scalars['UUID']>>>;
  query?: InputMaybe<Scalars['String']>;
};


export type QueryConvertorsDatasetGroupAttrsArgs = {
  datasetGroupId: Scalars['UUID'];
};


export type QueryConvertorsDatasetGroupsArgs = {
  query?: InputMaybe<Scalars['String']>;
};


export type QueryDatasetArgs = {
  id: Scalars['UUID'];
};


export type QueryDatasetGroupArgs = {
  id: Scalars['UUID'];
};


export type QueryDatasetGroupsArgs = {
  analyzed?: InputMaybe<Scalars['Boolean']>;
  keyword?: InputMaybe<Scalars['String']>;
  latest?: InputMaybe<Scalars['Boolean']>;
  page?: InputMaybe<Scalars['Int']>;
  pageSize?: InputMaybe<Scalars['Int']>;
  published?: InputMaybe<Scalars['Boolean']>;
};


export type QueryOwnDatasetGroupsArgs = {
  keyword?: InputMaybe<Scalars['String']>;
  page?: InputMaybe<Scalars['Int']>;
  pageSize?: InputMaybe<Scalars['Int']>;
};


export type QueryOwnTemplatesArgs = {
  page?: InputMaybe<Scalars['Int']>;
  pageSize?: InputMaybe<Scalars['Int']>;
};


export type QuerySimilarDatasetsArgs = {
  datasetGroupId: Scalars['String'];
  keyword?: InputMaybe<Scalars['String']>;
};


export type QuerySuggestByDatasetGroupArgs = {
  datasetGroupId: Scalars['UUID'];
  targetDatasetGroupId?: InputMaybe<Scalars['UUID']>;
};


export type QuerySuggestByDatasetTemplateArgs = {
  datasetGroupId: Scalars['UUID'];
  targetDatasetTemplateId?: InputMaybe<Scalars['UUID']>;
};


export type QueryTemplatesArgs = {
  createdById?: InputMaybe<Scalars['Boolean']>;
  keyword?: InputMaybe<Scalars['String']>;
  orderCreatedById?: InputMaybe<Scalars['Boolean']>;
  orderUpdatedAt?: InputMaybe<Scalars['Boolean']>;
};

export type Refresh = {
  __typename?: 'Refresh';
  payload: Scalars['GenericScalar'];
  refreshExpiresIn: Scalars['Int'];
  refreshToken: Scalars['String'];
  token: Scalars['String'];
};

export type Revoke = {
  __typename?: 'Revoke';
  revoked: Scalars['Int'];
};

export type SimilarDatasetType = {
  __typename?: 'SimilarDatasetType';
  datasetGroup?: Maybe<DatasetGroupType>;
  sim?: Maybe<Scalars['Float']>;
};

/** An enumeration. */
export enum StatusEnum {
  Fail = 'FAIL',
  Success = 'SUCCESS'
}

export type SuggestDatasetGroupType = {
  __typename?: 'SuggestDatasetGroupType';
  datasetGroup?: Maybe<DatasetGroupType>;
  id?: Maybe<Scalars['String']>;
  suggests?: Maybe<Array<Maybe<ConvertSuggestType>>>;
  targetDatasetGroup?: Maybe<DatasetGroupType>;
};

export type SuggestDatasetTemplateType = {
  __typename?: 'SuggestDatasetTemplateType';
  datasetGroup?: Maybe<DatasetGroupType>;
  id?: Maybe<Scalars['String']>;
  suggests?: Maybe<Array<Maybe<ConvertSuggestType>>>;
  targetDatasetTemplate?: Maybe<DatasetTemplateType>;
};

/** An enumeration. */
export enum TemplateStatusEnum {
  Fail = 'FAIL',
  Success = 'SUCCESS'
}

export type UpdateDatasetAttr = {
  __typename?: 'UpdateDatasetAttr';
  datasetAttr?: Maybe<DatasetAttrType>;
};

export type UpdateDatasetAttrInputType = {
  attrId: Scalars['UUID'];
  attrType?: InputMaybe<AttrTypeType>;
  dataType?: InputMaybe<DataTypeType>;
  index?: InputMaybe<Scalars['Int']>;
  name?: InputMaybe<Scalars['String']>;
};

export type UpdateDatasetGroup = {
  __typename?: 'UpdateDatasetGroup';
  datasetGroup?: Maybe<DatasetGroupType>;
};

export type UpdateDatasetGroupInputType = {
  createdBy?: InputMaybe<Scalars['String']>;
  currentDatasetId?: InputMaybe<Scalars['UUID']>;
  datasetGroupId: Scalars['UUID'];
  name?: InputMaybe<Scalars['String']>;
  originalFile?: InputMaybe<Scalars['Upload']>;
  publicLevel?: InputMaybe<Scalars['Int']>;
  source?: InputMaybe<DatasetSourceInputType>;
};

export type UpdateTemplate = {
  __typename?: 'UpdateTemplate';
  template?: Maybe<DatasetTemplateType>;
};

export type UpdateTemplateAttr = {
  __typename?: 'UpdateTemplateAttr';
  templateAttr?: Maybe<DatasetTemplateAttrType>;
};

export type UpdateTemplateAttrInputType = {
  attrId: Scalars['UUID'];
  attrType?: InputMaybe<AttrTypeType>;
  dataType?: InputMaybe<DataTypeType>;
  desc?: InputMaybe<Scalars['String']>;
  index?: InputMaybe<Scalars['Int']>;
  name?: InputMaybe<Scalars['String']>;
};

export type UpdateTemplateInputType = {
  desc?: InputMaybe<Scalars['String']>;
  name?: InputMaybe<Scalars['String']>;
  templateId: Scalars['UUID'];
};

export type UpdateUser = {
  __typename?: 'UpdateUser';
  user?: Maybe<UserType>;
};

export type UpdateUserInputType = {
  email?: InputMaybe<Scalars['String']>;
  name?: InputMaybe<Scalars['String']>;
  password?: InputMaybe<Scalars['String']>;
};

export type UserType = {
  __typename?: 'UserType';
  email: Scalars['String'];
  id: Scalars['UUID'];
  name: Scalars['String'];
};

export type Verify = {
  __typename?: 'Verify';
  payload: Scalars['GenericScalar'];
};

export type DatasetAttrFragmentFragment = { __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined };

export type DatasetFragmentFragment = { __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined };

export type DatasetGroupFragmentFragment = { __typename?: 'DatasetGroupType', id?: string | null | undefined, name?: string | null | undefined, originalFile?: string | null | undefined, publicLevelName?: string | null | undefined, publicLevel?: number | null | undefined, createdBy?: string | null | undefined, createdAt?: any | null | undefined, source?: { __typename?: 'DatasetSourceType', siteName?: string | null | undefined, siteUrl?: string | null | undefined } | null | undefined, currentDataset?: { __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined };

export type DatasetGroupFullyFragmentFragment = { __typename?: 'DatasetGroupType', id?: string | null | undefined, name?: string | null | undefined, originalFile?: string | null | undefined, createdBy?: string | null | undefined, createdAt?: any | null | undefined, publicLevel?: number | null | undefined, publicLevelName?: string | null | undefined, isOwner?: boolean | null | undefined, source?: { __typename?: 'DatasetSourceType', siteName?: string | null | undefined, siteUrl?: string | null | undefined } | null | undefined, currentDataset?: { __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined, datasets?: Array<{ __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined> | null | undefined };

export type DatasetTemplateAttrFragmentFragment = { __typename?: 'DatasetTemplateAttrType', id?: string | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined };

export type DatasetTemplateFragmentFragment = { __typename?: 'DatasetTemplateType', id?: any | null | undefined, name?: string | null | undefined, desc?: string | null | undefined, attrs?: Array<{ __typename?: 'DatasetTemplateAttrType', id?: string | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined };

export type TokenAuthMutationVariables = Exact<{
  email: Scalars['String'];
  password: Scalars['String'];
}>;


export type TokenAuthMutation = { __typename?: 'Mutation', tokenAuth?: { __typename?: 'ObtainJSONWebToken', payload: any, refreshExpiresIn: number, token: string, refreshToken: string } | null | undefined };

export type RefreshTokenMutationVariables = Exact<{
  refreshToken: Scalars['String'];
}>;


export type RefreshTokenMutation = { __typename?: 'Mutation', refreshToken?: { __typename?: 'Refresh', payload: any, token: string, refreshToken: string } | null | undefined };

export type VerifyTokenMutationVariables = Exact<{
  token: Scalars['String'];
}>;


export type VerifyTokenMutation = { __typename?: 'Mutation', verifyToken?: { __typename?: 'Verify', payload: any } | null | undefined };

export type UpdateDatasetAttrMutationVariables = Exact<{
  input: UpdateDatasetAttrInputType;
}>;


export type UpdateDatasetAttrMutation = { __typename?: 'Mutation', updateDatasetAttr?: { __typename?: 'UpdateDatasetAttr', datasetAttr?: { __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined } | null | undefined };

export type CreateConvertJobMutationVariables = Exact<{
  input: CreateConvertJobInputType;
}>;


export type CreateConvertJobMutation = { __typename?: 'Mutation', createConvertJob?: { __typename?: 'CreateConvertJob', status?: JobStatusEnum | null | undefined, datasetConvertJob?: { __typename?: 'DatasetConvertJobType', filterKey?: string | null | undefined, taskId?: string | null | undefined, result?: string | null | undefined, status?: string | null | undefined, hasError?: string | null | undefined, errors?: any | null | undefined, errorMessages?: Array<string | null | undefined> | null | undefined, dataset?: { __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined } | null | undefined } | null | undefined };

export type ConvertPreviewMutationVariables = Exact<{
  input: CreatePreviewInputType;
}>;


export type ConvertPreviewMutation = { __typename?: 'Mutation', createConvertPreview?: { __typename?: 'CreateConvertPreview', status?: PreviewStatusEnum | null | undefined, datasetPreview?: { __typename?: 'DatasetPreviewType', filterKey?: string | null | undefined, taskId?: string | null | undefined, result?: string | null | undefined, status?: string | null | undefined, hasError?: boolean | null | undefined, errors?: any | null | undefined, errorMessages?: Array<string | null | undefined> | null | undefined, dataset?: { __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined } | null | undefined } | null | undefined };

export type AnalyzeDatasetGroupMutationVariables = Exact<{
  input: AnalyzeDatasetGroupInputType;
}>;


export type AnalyzeDatasetGroupMutation = { __typename?: 'Mutation', analyzeDatasetGroup?: { __typename?: 'AnalyzeDatasetGroup', datasetGroup?: { __typename?: 'DatasetGroupType', id?: string | null | undefined, originalFile?: string | null | undefined, source?: { __typename?: 'DatasetSourceType', siteName?: string | null | undefined, siteUrl?: string | null | undefined } | null | undefined, currentDataset?: { __typename?: 'DatasetType', numRecords?: number | null | undefined, numColumns?: number | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, name?: string | null | undefined } | null | undefined> | null | undefined } | null | undefined } | null | undefined } | null | undefined };

export type CreateDatasetGroupMutationVariables = Exact<{
  input: CreateDatasetGroupInputType;
}>;


export type CreateDatasetGroupMutation = { __typename?: 'Mutation', createDatasetGroup?: { __typename?: 'CreateDatasetGroup', datasetGroup?: { __typename?: 'DatasetGroupType', id?: string | null | undefined, originalFile?: string | null | undefined, source?: { __typename?: 'DatasetSourceType', siteName?: string | null | undefined, siteUrl?: string | null | undefined } | null | undefined, currentDataset?: { __typename?: 'DatasetType', numRecords?: number | null | undefined, numColumns?: number | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, name?: string | null | undefined } | null | undefined> | null | undefined } | null | undefined } | null | undefined } | null | undefined };

export type DeleteDatasetGroupMutationVariables = Exact<{
  datasetGroupId: Scalars['UUID'];
}>;


export type DeleteDatasetGroupMutation = { __typename?: 'Mutation', deleteDatasetGroup?: { __typename?: 'DeleteDatasetGroup', status?: StatusEnum | null | undefined } | null | undefined };

export type UpdateDatasetGroupMutationVariables = Exact<{
  input: UpdateDatasetGroupInputType;
}>;


export type UpdateDatasetGroupMutation = { __typename?: 'Mutation', updateDatasetGroup?: { __typename?: 'UpdateDatasetGroup', datasetGroup?: { __typename?: 'DatasetGroupType', id?: string | null | undefined, originalFile?: string | null | undefined, source?: { __typename?: 'DatasetSourceType', siteName?: string | null | undefined, siteUrl?: string | null | undefined } | null | undefined, currentDataset?: { __typename?: 'DatasetType', numRecords?: number | null | undefined, numColumns?: number | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, name?: string | null | undefined } | null | undefined> | null | undefined } | null | undefined } | null | undefined } | null | undefined };

export type PasswordResetRequestMutationVariables = Exact<{
  email: Scalars['String'];
}>;


export type PasswordResetRequestMutation = { __typename?: 'Mutation', passwordResetRequest?: { __typename?: 'PasswordResetRequest', user?: { __typename?: 'UserType', id: any } | null | undefined } | null | undefined };

export type PasswordResetMutationVariables = Exact<{
  password: Scalars['String'];
  passwordResetToken: Scalars['String'];
}>;


export type PasswordResetMutation = { __typename?: 'Mutation', passwordReset?: { __typename?: 'PasswordReset', user?: { __typename?: 'UserType', id: any } | null | undefined } | null | undefined };

export type CreateUserMutationVariables = Exact<{
  input: CreateUserInputType;
}>;


export type CreateUserMutation = { __typename?: 'Mutation', createUser?: { __typename?: 'CreateUser', user?: { __typename?: 'UserType', id: any, name: string, email: string } | null | undefined } | null | undefined };

export type UpdateUserMutationVariables = Exact<{
  input: UpdateUserInputType;
}>;


export type UpdateUserMutation = { __typename?: 'Mutation', updateUser?: { __typename?: 'UpdateUser', user?: { __typename?: 'UserType', id: any, name: string, email: string } | null | undefined } | null | undefined };

export type GetManyAttrTypeQueryVariables = Exact<{ [key: string]: never; }>;


export type GetManyAttrTypeQuery = { __typename?: 'Query', attrTypes?: Array<{ __typename?: 'EnumType', name?: string | null | undefined, value?: string | null | undefined } | null | undefined> | null | undefined };

export type GetManyConvertorFiltersQueryVariables = Exact<{
  datasetAttrIds?: InputMaybe<Array<InputMaybe<Scalars['UUID']>> | InputMaybe<Scalars['UUID']>>;
  query?: InputMaybe<Scalars['String']>;
}>;


export type GetManyConvertorFiltersQuery = { __typename?: 'Query', convertorFilters?: Array<{ __typename?: 'FilterType', key?: string | null | undefined, name?: string | null | undefined, description?: string | null | undefined, helpText?: string | null | undefined, params?: Array<{ __typename?: 'ParamType', name?: string | null | undefined, description?: string | null | undefined, helpText?: string | null | undefined, group?: string | null | undefined, defaultValue?: string | null | undefined, label?: string | null | undefined, required?: boolean | null | undefined, type?: string | null | undefined, arguments?: any | null | undefined } | null | undefined> | null | undefined } | null | undefined> | null | undefined };

export type GetManyDataTypeQueryVariables = Exact<{ [key: string]: never; }>;


export type GetManyDataTypeQuery = { __typename?: 'Query', dataTypes?: Array<{ __typename?: 'EnumType', name?: string | null | undefined, value?: string | null | undefined } | null | undefined> | null | undefined };

export type DatasetGroupsQueryVariables = Exact<{
  analyzed?: InputMaybe<Scalars['Boolean']>;
  published?: InputMaybe<Scalars['Boolean']>;
  latest?: InputMaybe<Scalars['Boolean']>;
  keyword?: InputMaybe<Scalars['String']>;
  page?: InputMaybe<Scalars['Int']>;
  pageSize?: InputMaybe<Scalars['Int']>;
}>;


export type DatasetGroupsQuery = { __typename?: 'Query', datasetGroups?: { __typename?: 'DatasetGroupListType', keyword?: string | null | undefined, page?: number | null | undefined, pageSize?: number | null | undefined, totalRecords?: number | null | undefined, datasetGroups?: Array<{ __typename?: 'DatasetGroupType', id?: string | null | undefined, name?: string | null | undefined, originalFile?: string | null | undefined, publicLevelName?: string | null | undefined, publicLevel?: number | null | undefined, createdBy?: string | null | undefined, createdAt?: any | null | undefined, source?: { __typename?: 'DatasetSourceType', siteName?: string | null | undefined, siteUrl?: string | null | undefined } | null | undefined, currentDataset?: { __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined } | null | undefined> | null | undefined } | null | undefined };

export type DatasetGroupQueryVariables = Exact<{
  id: Scalars['UUID'];
}>;


export type DatasetGroupQuery = { __typename?: 'Query', datasetGroup?: { __typename?: 'DatasetGroupType', id?: string | null | undefined, name?: string | null | undefined, originalFile?: string | null | undefined, createdBy?: string | null | undefined, createdAt?: any | null | undefined, publicLevel?: number | null | undefined, publicLevelName?: string | null | undefined, isOwner?: boolean | null | undefined, source?: { __typename?: 'DatasetSourceType', siteName?: string | null | undefined, siteUrl?: string | null | undefined } | null | undefined, currentDataset?: { __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined, datasets?: Array<{ __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined };

export type SimilarDatasetsQueryVariables = Exact<{
  datasetGroupId: Scalars['String'];
  keyword?: InputMaybe<Scalars['String']>;
}>;


export type SimilarDatasetsQuery = { __typename?: 'Query', similarDatasets?: Array<{ __typename?: 'SimilarDatasetType', sim?: number | null | undefined, datasetGroup?: { __typename?: 'DatasetGroupType', id?: string | null | undefined, name?: string | null | undefined, originalFile?: string | null | undefined, createdBy?: string | null | undefined, createdAt?: any | null | undefined, source?: { __typename?: 'DatasetSourceType', siteName?: string | null | undefined, siteUrl?: string | null | undefined } | null | undefined, currentDataset?: { __typename?: 'DatasetType', numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, name?: string | null | undefined } | null | undefined> | null | undefined } | null | undefined } | null | undefined } | null | undefined> | null | undefined };

export type GetDatasetQueryVariables = Exact<{
  id: Scalars['UUID'];
}>;


export type GetDatasetQuery = { __typename?: 'Query', dataset?: { __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined };

export type OwnDatasetGroupsQueryVariables = Exact<{
  keyword?: InputMaybe<Scalars['String']>;
  page?: InputMaybe<Scalars['Int']>;
  pageSize?: InputMaybe<Scalars['Int']>;
}>;


export type OwnDatasetGroupsQuery = { __typename?: 'Query', ownDatasetGroups?: { __typename?: 'DatasetGroupListType', keyword?: string | null | undefined, page?: number | null | undefined, pageSize?: number | null | undefined, totalRecords?: number | null | undefined, datasetGroups?: Array<{ __typename?: 'DatasetGroupType', id?: string | null | undefined, name?: string | null | undefined, originalFile?: string | null | undefined, publicLevelName?: string | null | undefined, publicLevel?: number | null | undefined, createdBy?: string | null | undefined, createdAt?: any | null | undefined, source?: { __typename?: 'DatasetSourceType', siteName?: string | null | undefined, siteUrl?: string | null | undefined } | null | undefined, currentDataset?: { __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined } | null | undefined> | null | undefined } | null | undefined };

export type GetOwnUserQueryVariables = Exact<{ [key: string]: never; }>;


export type GetOwnUserQuery = { __typename?: 'Query', ownUser?: { __typename?: 'UserType', name: string, email: string } | null | undefined };

export type GetManySuggestsByDatasetGroupQueryVariables = Exact<{
  datasetGroupId: Scalars['UUID'];
  targetDatasetGroupId?: InputMaybe<Scalars['UUID']>;
}>;


export type GetManySuggestsByDatasetGroupQuery = { __typename?: 'Query', suggestByDatasetGroup?: { __typename?: 'SuggestDatasetGroupType', datasetGroup?: { __typename?: 'DatasetGroupType', id?: string | null | undefined, name?: string | null | undefined, originalFile?: string | null | undefined, createdBy?: string | null | undefined, createdAt?: any | null | undefined, publicLevel?: number | null | undefined, publicLevelName?: string | null | undefined, isOwner?: boolean | null | undefined, source?: { __typename?: 'DatasetSourceType', siteName?: string | null | undefined, siteUrl?: string | null | undefined } | null | undefined, currentDataset?: { __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined, datasets?: Array<{ __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined, targetDatasetGroup?: { __typename?: 'DatasetGroupType', id?: string | null | undefined, name?: string | null | undefined, originalFile?: string | null | undefined, createdBy?: string | null | undefined, createdAt?: any | null | undefined, publicLevel?: number | null | undefined, publicLevelName?: string | null | undefined, isOwner?: boolean | null | undefined, source?: { __typename?: 'DatasetSourceType', siteName?: string | null | undefined, siteUrl?: string | null | undefined } | null | undefined, currentDataset?: { __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined, datasets?: Array<{ __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined, suggests?: Array<{ __typename?: 'ConvertSuggestType', sourceIndex?: number | null | undefined, title?: string | null | undefined, message?: string | null | undefined, filterKey: string, filterParams: string } | null | undefined> | null | undefined } | null | undefined };

export type GetManySuggestsByDatasetTemplateQueryVariables = Exact<{
  datasetGroupId: Scalars['UUID'];
  targetDatasetTemplateId?: InputMaybe<Scalars['UUID']>;
}>;


export type GetManySuggestsByDatasetTemplateQuery = { __typename?: 'Query', suggestByDatasetTemplate?: { __typename?: 'SuggestDatasetTemplateType', datasetGroup?: { __typename?: 'DatasetGroupType', id?: string | null | undefined, name?: string | null | undefined, originalFile?: string | null | undefined, createdBy?: string | null | undefined, createdAt?: any | null | undefined, publicLevel?: number | null | undefined, publicLevelName?: string | null | undefined, isOwner?: boolean | null | undefined, source?: { __typename?: 'DatasetSourceType', siteName?: string | null | undefined, siteUrl?: string | null | undefined } | null | undefined, currentDataset?: { __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined, datasets?: Array<{ __typename?: 'DatasetType', id?: string | null | undefined, name?: string | null | undefined, numRecords?: number | null | undefined, numColumns?: number | null | undefined, analyzedStatus?: number | null | undefined, isAnalyzed?: boolean | null | undefined, hasAnnotates?: boolean | null | undefined, annotateMessages?: Array<string | null | undefined> | null | undefined, fileSize?: number | null | undefined, filterJson?: string | null | undefined, filterDetail?: string | null | undefined, attrNames?: Array<string | null | undefined> | null | undefined, dataFile?: string | null | undefined, dataFileUrl?: string | null | undefined, version?: number | null | undefined, createdAt?: any | null | undefined, attrs?: Array<{ __typename?: 'DatasetAttrType', id?: any | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined, targetDatasetTemplate?: { __typename?: 'DatasetTemplateType', id?: any | null | undefined, name?: string | null | undefined, desc?: string | null | undefined, attrs?: Array<{ __typename?: 'DatasetTemplateAttrType', id?: string | null | undefined, index?: number | null | undefined, no?: number | null | undefined, name?: string | null | undefined, attrType?: AttrTypeType | null | undefined, attrTypeName?: string | null | undefined, dataType?: DataTypeType | null | undefined, dataTypeName?: string | null | undefined, sampleValues?: Array<string | null | undefined> | null | undefined } | null | undefined> | null | undefined } | null | undefined, suggests?: Array<{ __typename?: 'ConvertSuggestType', sourceIndex?: number | null | undefined, title?: string | null | undefined, message?: string | null | undefined, filterKey: string, filterParams: string } | null | undefined> | null | undefined } | null | undefined };

export type TemplatesQueryVariables = Exact<{
  keyword?: InputMaybe<Scalars['String']>;
}>;


export type TemplatesQuery = { __typename?: 'Query', templates?: Array<{ __typename?: 'DatasetTemplateType', id?: any | null | undefined, name?: string | null | undefined, desc?: string | null | undefined, attrs?: Array<{ __typename?: 'DatasetTemplateAttrType', id?: string | null | undefined, name?: string | null | undefined } | null | undefined> | null | undefined } | null | undefined> | null | undefined };

export type OwnUserQueryVariables = Exact<{ [key: string]: never; }>;


export type OwnUserQuery = { __typename?: 'Query', ownUser?: { __typename?: 'UserType', id: any, name: string, email: string } | null | undefined };
