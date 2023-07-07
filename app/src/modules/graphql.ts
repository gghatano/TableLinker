/* eslint-disable */
import * as schema from "@/schema/schema";

import gql from 'graphql-tag';
import * as VueApolloComposable from '@vue/apollo-composable';
import * as VueCompositionApi from 'vue';
export type ReactiveFunction<TParam> = () => TParam;
export const DatasetAttrFragmentFragmentDoc = gql`
    fragment DatasetAttrFragment on DatasetAttrType {
  id
  index
  no
  name
  attrType
  attrTypeName
  dataType
  dataTypeName
  sampleValues
}
    `;
export const DatasetFragmentFragmentDoc = gql`
    fragment DatasetFragment on DatasetType {
  id
  name
  numRecords
  numColumns
  analyzedStatus
  isAnalyzed
  hasAnnotates
  annotateMessages
  fileSize
  filterJson
  filterDetail
  attrNames
  dataFile
  dataFileUrl
  version
  createdAt
  attrs {
    ...DatasetAttrFragment
  }
}
    ${DatasetAttrFragmentFragmentDoc}`;
export const DatasetGroupFragmentFragmentDoc = gql`
    fragment DatasetGroupFragment on DatasetGroupType {
  id
  name
  source {
    siteName
    siteUrl
  }
  originalFile
  publicLevelName
  publicLevel
  createdBy
  createdAt
  currentDataset {
    ...DatasetFragment
  }
}
    ${DatasetFragmentFragmentDoc}`;
export const DatasetGroupFullyFragmentFragmentDoc = gql`
    fragment DatasetGroupFullyFragment on DatasetGroupType {
  id
  name
  source {
    siteName
    siteUrl
  }
  originalFile
  createdBy
  createdAt
  publicLevel
  publicLevelName
  isOwner
  currentDataset {
    ...DatasetFragment
  }
  datasets {
    ...DatasetFragment
  }
}
    ${DatasetFragmentFragmentDoc}`;
export const DatasetTemplateAttrFragmentFragmentDoc = gql`
    fragment DatasetTemplateAttrFragment on DatasetTemplateAttrType {
  id
  index
  no
  name
  attrType
  attrTypeName
  dataType
  dataTypeName
  sampleValues
}
    `;
export const DatasetTemplateFragmentFragmentDoc = gql`
    fragment DatasetTemplateFragment on DatasetTemplateType {
  id
  name
  desc
  attrs {
    ...DatasetTemplateAttrFragment
  }
}
    ${DatasetTemplateAttrFragmentFragmentDoc}`;
export const TokenAuthDocument = gql`
    mutation tokenAuth($email: String!, $password: String!) {
  tokenAuth(email: $email, password: $password) {
    payload
    refreshExpiresIn
    token
    refreshToken
  }
}
    `;

/**
 * __useTokenAuthMutation__
 *
 * To run a mutation, you first call `useTokenAuthMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useTokenAuthMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useTokenAuthMutation({
 *   variables: {
 *     email: // value for 'email'
 *     password: // value for 'password'
 *   },
 * });
 */
export function useTokenAuthMutation(options: VueApolloComposable.UseMutationOptions<schema.TokenAuthMutation, schema.TokenAuthMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.TokenAuthMutation, schema.TokenAuthMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.TokenAuthMutation, schema.TokenAuthMutationVariables>(TokenAuthDocument, options);
}
export type TokenAuthMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.TokenAuthMutation, schema.TokenAuthMutationVariables>;
export const RefreshTokenDocument = gql`
    mutation refreshToken($refreshToken: String!) {
  refreshToken(refreshToken: $refreshToken) {
    payload
    token
    refreshToken
  }
}
    `;

/**
 * __useRefreshTokenMutation__
 *
 * To run a mutation, you first call `useRefreshTokenMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useRefreshTokenMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useRefreshTokenMutation({
 *   variables: {
 *     refreshToken: // value for 'refreshToken'
 *   },
 * });
 */
export function useRefreshTokenMutation(options: VueApolloComposable.UseMutationOptions<schema.RefreshTokenMutation, schema.RefreshTokenMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.RefreshTokenMutation, schema.RefreshTokenMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.RefreshTokenMutation, schema.RefreshTokenMutationVariables>(RefreshTokenDocument, options);
}
export type RefreshTokenMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.RefreshTokenMutation, schema.RefreshTokenMutationVariables>;
export const VerifyTokenDocument = gql`
    mutation verifyToken($token: String!) {
  verifyToken(token: $token) {
    payload
  }
}
    `;

/**
 * __useVerifyTokenMutation__
 *
 * To run a mutation, you first call `useVerifyTokenMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useVerifyTokenMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useVerifyTokenMutation({
 *   variables: {
 *     token: // value for 'token'
 *   },
 * });
 */
export function useVerifyTokenMutation(options: VueApolloComposable.UseMutationOptions<schema.VerifyTokenMutation, schema.VerifyTokenMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.VerifyTokenMutation, schema.VerifyTokenMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.VerifyTokenMutation, schema.VerifyTokenMutationVariables>(VerifyTokenDocument, options);
}
export type VerifyTokenMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.VerifyTokenMutation, schema.VerifyTokenMutationVariables>;
export const UpdateDatasetAttrDocument = gql`
    mutation updateDatasetAttr($input: UpdateDatasetAttrInputType!) {
  updateDatasetAttr(input: $input) {
    datasetAttr {
      ...DatasetAttrFragment
    }
  }
}
    ${DatasetAttrFragmentFragmentDoc}`;

/**
 * __useUpdateDatasetAttrMutation__
 *
 * To run a mutation, you first call `useUpdateDatasetAttrMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useUpdateDatasetAttrMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useUpdateDatasetAttrMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useUpdateDatasetAttrMutation(options: VueApolloComposable.UseMutationOptions<schema.UpdateDatasetAttrMutation, schema.UpdateDatasetAttrMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.UpdateDatasetAttrMutation, schema.UpdateDatasetAttrMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.UpdateDatasetAttrMutation, schema.UpdateDatasetAttrMutationVariables>(UpdateDatasetAttrDocument, options);
}
export type UpdateDatasetAttrMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.UpdateDatasetAttrMutation, schema.UpdateDatasetAttrMutationVariables>;
export const CreateConvertJobDocument = gql`
    mutation CreateConvertJob($input: CreateConvertJobInputType!) {
  createConvertJob(input: $input) {
    datasetConvertJob {
      dataset {
        ...DatasetFragment
      }
      filterKey
      taskId
      result
      status
      hasError
      errors
      errorMessages
    }
    status
  }
}
    ${DatasetFragmentFragmentDoc}`;

/**
 * __useCreateConvertJobMutation__
 *
 * To run a mutation, you first call `useCreateConvertJobMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useCreateConvertJobMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useCreateConvertJobMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useCreateConvertJobMutation(options: VueApolloComposable.UseMutationOptions<schema.CreateConvertJobMutation, schema.CreateConvertJobMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.CreateConvertJobMutation, schema.CreateConvertJobMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.CreateConvertJobMutation, schema.CreateConvertJobMutationVariables>(CreateConvertJobDocument, options);
}
export type CreateConvertJobMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.CreateConvertJobMutation, schema.CreateConvertJobMutationVariables>;
export const ConvertPreviewDocument = gql`
    mutation ConvertPreview($input: CreatePreviewInputType!) {
  createConvertPreview(input: $input) {
    datasetPreview {
      dataset {
        ...DatasetFragment
      }
      filterKey
      taskId
      result
      status
      hasError
      errors
      errorMessages
    }
    status
  }
}
    ${DatasetFragmentFragmentDoc}`;

/**
 * __useConvertPreviewMutation__
 *
 * To run a mutation, you first call `useConvertPreviewMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useConvertPreviewMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useConvertPreviewMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useConvertPreviewMutation(options: VueApolloComposable.UseMutationOptions<schema.ConvertPreviewMutation, schema.ConvertPreviewMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.ConvertPreviewMutation, schema.ConvertPreviewMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.ConvertPreviewMutation, schema.ConvertPreviewMutationVariables>(ConvertPreviewDocument, options);
}
export type ConvertPreviewMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.ConvertPreviewMutation, schema.ConvertPreviewMutationVariables>;
export const AnalyzeDatasetGroupDocument = gql`
    mutation AnalyzeDatasetGroup($input: AnalyzeDatasetGroupInputType!) {
  analyzeDatasetGroup(input: $input) {
    datasetGroup {
      id
      source {
        siteName
        siteUrl
      }
      originalFile
      currentDataset {
        numRecords
        numColumns
        fileSize
        filterJson
        attrNames
        dataFile
        version
        createdAt
        attrs {
          id
          index
          name
        }
      }
    }
  }
}
    `;

/**
 * __useAnalyzeDatasetGroupMutation__
 *
 * To run a mutation, you first call `useAnalyzeDatasetGroupMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useAnalyzeDatasetGroupMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useAnalyzeDatasetGroupMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useAnalyzeDatasetGroupMutation(options: VueApolloComposable.UseMutationOptions<schema.AnalyzeDatasetGroupMutation, schema.AnalyzeDatasetGroupMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.AnalyzeDatasetGroupMutation, schema.AnalyzeDatasetGroupMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.AnalyzeDatasetGroupMutation, schema.AnalyzeDatasetGroupMutationVariables>(AnalyzeDatasetGroupDocument, options);
}
export type AnalyzeDatasetGroupMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.AnalyzeDatasetGroupMutation, schema.AnalyzeDatasetGroupMutationVariables>;
export const CreateDatasetGroupDocument = gql`
    mutation createDatasetGroup($input: CreateDatasetGroupInputType!) {
  createDatasetGroup(input: $input) {
    datasetGroup {
      id
      source {
        siteName
        siteUrl
      }
      originalFile
      currentDataset {
        numRecords
        numColumns
        fileSize
        filterJson
        attrNames
        dataFile
        version
        createdAt
        attrs {
          id
          index
          name
        }
      }
    }
  }
}
    `;

/**
 * __useCreateDatasetGroupMutation__
 *
 * To run a mutation, you first call `useCreateDatasetGroupMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useCreateDatasetGroupMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useCreateDatasetGroupMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useCreateDatasetGroupMutation(options: VueApolloComposable.UseMutationOptions<schema.CreateDatasetGroupMutation, schema.CreateDatasetGroupMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.CreateDatasetGroupMutation, schema.CreateDatasetGroupMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.CreateDatasetGroupMutation, schema.CreateDatasetGroupMutationVariables>(CreateDatasetGroupDocument, options);
}
export type CreateDatasetGroupMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.CreateDatasetGroupMutation, schema.CreateDatasetGroupMutationVariables>;
export const DeleteDatasetGroupDocument = gql`
    mutation deleteDatasetGroup($datasetGroupId: UUID!) {
  deleteDatasetGroup(datasetGroupId: $datasetGroupId) {
    status
  }
}
    `;

/**
 * __useDeleteDatasetGroupMutation__
 *
 * To run a mutation, you first call `useDeleteDatasetGroupMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useDeleteDatasetGroupMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useDeleteDatasetGroupMutation({
 *   variables: {
 *     datasetGroupId: // value for 'datasetGroupId'
 *   },
 * });
 */
export function useDeleteDatasetGroupMutation(options: VueApolloComposable.UseMutationOptions<schema.DeleteDatasetGroupMutation, schema.DeleteDatasetGroupMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.DeleteDatasetGroupMutation, schema.DeleteDatasetGroupMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.DeleteDatasetGroupMutation, schema.DeleteDatasetGroupMutationVariables>(DeleteDatasetGroupDocument, options);
}
export type DeleteDatasetGroupMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.DeleteDatasetGroupMutation, schema.DeleteDatasetGroupMutationVariables>;
export const UpdateDatasetGroupDocument = gql`
    mutation updateDatasetGroup($input: UpdateDatasetGroupInputType!) {
  updateDatasetGroup(input: $input) {
    datasetGroup {
      id
      source {
        siteName
        siteUrl
      }
      originalFile
      currentDataset {
        numRecords
        numColumns
        fileSize
        filterJson
        attrNames
        dataFile
        version
        createdAt
        attrs {
          id
          index
          name
        }
      }
    }
  }
}
    `;

/**
 * __useUpdateDatasetGroupMutation__
 *
 * To run a mutation, you first call `useUpdateDatasetGroupMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useUpdateDatasetGroupMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useUpdateDatasetGroupMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useUpdateDatasetGroupMutation(options: VueApolloComposable.UseMutationOptions<schema.UpdateDatasetGroupMutation, schema.UpdateDatasetGroupMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.UpdateDatasetGroupMutation, schema.UpdateDatasetGroupMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.UpdateDatasetGroupMutation, schema.UpdateDatasetGroupMutationVariables>(UpdateDatasetGroupDocument, options);
}
export type UpdateDatasetGroupMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.UpdateDatasetGroupMutation, schema.UpdateDatasetGroupMutationVariables>;
export const PasswordResetRequestDocument = gql`
    mutation passwordResetRequest($email: String!) {
  passwordResetRequest(email: $email) {
    user {
      id
    }
  }
}
    `;

/**
 * __usePasswordResetRequestMutation__
 *
 * To run a mutation, you first call `usePasswordResetRequestMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `usePasswordResetRequestMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = usePasswordResetRequestMutation({
 *   variables: {
 *     email: // value for 'email'
 *   },
 * });
 */
export function usePasswordResetRequestMutation(options: VueApolloComposable.UseMutationOptions<schema.PasswordResetRequestMutation, schema.PasswordResetRequestMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.PasswordResetRequestMutation, schema.PasswordResetRequestMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.PasswordResetRequestMutation, schema.PasswordResetRequestMutationVariables>(PasswordResetRequestDocument, options);
}
export type PasswordResetRequestMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.PasswordResetRequestMutation, schema.PasswordResetRequestMutationVariables>;
export const PasswordResetDocument = gql`
    mutation passwordReset($password: String!, $passwordResetToken: String!) {
  passwordReset(password: $password, passwordResetToken: $passwordResetToken) {
    user {
      id
    }
  }
}
    `;

/**
 * __usePasswordResetMutation__
 *
 * To run a mutation, you first call `usePasswordResetMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `usePasswordResetMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = usePasswordResetMutation({
 *   variables: {
 *     password: // value for 'password'
 *     passwordResetToken: // value for 'passwordResetToken'
 *   },
 * });
 */
export function usePasswordResetMutation(options: VueApolloComposable.UseMutationOptions<schema.PasswordResetMutation, schema.PasswordResetMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.PasswordResetMutation, schema.PasswordResetMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.PasswordResetMutation, schema.PasswordResetMutationVariables>(PasswordResetDocument, options);
}
export type PasswordResetMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.PasswordResetMutation, schema.PasswordResetMutationVariables>;
export const CreateUserDocument = gql`
    mutation createUser($input: CreateUserInputType!) {
  createUser(input: $input) {
    user {
      id
      name
      email
    }
  }
}
    `;

/**
 * __useCreateUserMutation__
 *
 * To run a mutation, you first call `useCreateUserMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useCreateUserMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useCreateUserMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useCreateUserMutation(options: VueApolloComposable.UseMutationOptions<schema.CreateUserMutation, schema.CreateUserMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.CreateUserMutation, schema.CreateUserMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.CreateUserMutation, schema.CreateUserMutationVariables>(CreateUserDocument, options);
}
export type CreateUserMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.CreateUserMutation, schema.CreateUserMutationVariables>;
export const UpdateUserDocument = gql`
    mutation updateUser($input: UpdateUserInputType!) {
  updateUser(input: $input) {
    user {
      id
      name
      email
    }
  }
}
    `;

/**
 * __useUpdateUserMutation__
 *
 * To run a mutation, you first call `useUpdateUserMutation` within a Vue component and pass it any options that fit your needs.
 * When your component renders, `useUpdateUserMutation` returns an object that includes:
 * - A mutate function that you can call at any time to execute the mutation
 * - Several other properties: https://v4.apollo.vuejs.org/api/use-mutation.html#return
 *
 * @param options that will be passed into the mutation, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/mutation.html#options;
 *
 * @example
 * const { mutate, loading, error, onDone } = useUpdateUserMutation({
 *   variables: {
 *     input: // value for 'input'
 *   },
 * });
 */
export function useUpdateUserMutation(options: VueApolloComposable.UseMutationOptions<schema.UpdateUserMutation, schema.UpdateUserMutationVariables> | ReactiveFunction<VueApolloComposable.UseMutationOptions<schema.UpdateUserMutation, schema.UpdateUserMutationVariables>>) {
  return VueApolloComposable.useMutation<schema.UpdateUserMutation, schema.UpdateUserMutationVariables>(UpdateUserDocument, options);
}
export type UpdateUserMutationCompositionFunctionResult = VueApolloComposable.UseMutationReturn<schema.UpdateUserMutation, schema.UpdateUserMutationVariables>;
export const GetManyAttrTypeDocument = gql`
    query GetManyAttrType {
  attrTypes {
    name
    value
  }
}
    `;

/**
 * __useGetManyAttrTypeQuery__
 *
 * To run a query within a Vue component, call `useGetManyAttrTypeQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetManyAttrTypeQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useGetManyAttrTypeQuery();
 */
export function useGetManyAttrTypeQuery(options: VueApolloComposable.UseQueryOptions<schema.GetManyAttrTypeQuery, schema.GetManyAttrTypeQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.GetManyAttrTypeQuery, schema.GetManyAttrTypeQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.GetManyAttrTypeQuery, schema.GetManyAttrTypeQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.GetManyAttrTypeQuery, schema.GetManyAttrTypeQueryVariables>(GetManyAttrTypeDocument, {}, options);
}
export type GetManyAttrTypeQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.GetManyAttrTypeQuery, schema.GetManyAttrTypeQueryVariables>;
export const GetManyConvertorFiltersDocument = gql`
    query GetManyConvertorFilters($datasetAttrIds: [UUID], $query: String) {
  convertorFilters(datasetAttrIds: $datasetAttrIds, query: $query) {
    key
    name
    description
    helpText
    params {
      name
      description
      helpText
      group
      defaultValue
      label
      required
      type
      arguments
    }
  }
}
    `;

/**
 * __useGetManyConvertorFiltersQuery__
 *
 * To run a query within a Vue component, call `useGetManyConvertorFiltersQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetManyConvertorFiltersQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useGetManyConvertorFiltersQuery({
 *   datasetAttrIds: // value for 'datasetAttrIds'
 *   query: // value for 'query'
 * });
 */
export function useGetManyConvertorFiltersQuery(variables: schema.GetManyConvertorFiltersQueryVariables | VueCompositionApi.Ref<schema.GetManyConvertorFiltersQueryVariables> | ReactiveFunction<schema.GetManyConvertorFiltersQueryVariables> = {}, options: VueApolloComposable.UseQueryOptions<schema.GetManyConvertorFiltersQuery, schema.GetManyConvertorFiltersQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.GetManyConvertorFiltersQuery, schema.GetManyConvertorFiltersQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.GetManyConvertorFiltersQuery, schema.GetManyConvertorFiltersQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.GetManyConvertorFiltersQuery, schema.GetManyConvertorFiltersQueryVariables>(GetManyConvertorFiltersDocument, variables, options);
}
export type GetManyConvertorFiltersQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.GetManyConvertorFiltersQuery, schema.GetManyConvertorFiltersQueryVariables>;
export const GetManyDataTypeDocument = gql`
    query GetManyDataType {
  dataTypes {
    name
    value
  }
}
    `;

/**
 * __useGetManyDataTypeQuery__
 *
 * To run a query within a Vue component, call `useGetManyDataTypeQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetManyDataTypeQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useGetManyDataTypeQuery();
 */
export function useGetManyDataTypeQuery(options: VueApolloComposable.UseQueryOptions<schema.GetManyDataTypeQuery, schema.GetManyDataTypeQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.GetManyDataTypeQuery, schema.GetManyDataTypeQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.GetManyDataTypeQuery, schema.GetManyDataTypeQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.GetManyDataTypeQuery, schema.GetManyDataTypeQueryVariables>(GetManyDataTypeDocument, {}, options);
}
export type GetManyDataTypeQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.GetManyDataTypeQuery, schema.GetManyDataTypeQueryVariables>;
export const DatasetGroupsDocument = gql`
    query datasetGroups($analyzed: Boolean, $published: Boolean, $latest: Boolean, $keyword: String, $page: Int, $pageSize: Int) {
  datasetGroups(
    analyzed: $analyzed
    published: $published
    latest: $latest
    keyword: $keyword
    page: $page
    pageSize: $pageSize
  ) {
    keyword
    page
    pageSize
    totalRecords
    datasetGroups {
      ...DatasetGroupFragment
    }
  }
}
    ${DatasetGroupFragmentFragmentDoc}`;

/**
 * __useDatasetGroupsQuery__
 *
 * To run a query within a Vue component, call `useDatasetGroupsQuery` and pass it any options that fit your needs.
 * When your component renders, `useDatasetGroupsQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useDatasetGroupsQuery({
 *   analyzed: // value for 'analyzed'
 *   published: // value for 'published'
 *   latest: // value for 'latest'
 *   keyword: // value for 'keyword'
 *   page: // value for 'page'
 *   pageSize: // value for 'pageSize'
 * });
 */
export function useDatasetGroupsQuery(variables: schema.DatasetGroupsQueryVariables | VueCompositionApi.Ref<schema.DatasetGroupsQueryVariables> | ReactiveFunction<schema.DatasetGroupsQueryVariables> = {}, options: VueApolloComposable.UseQueryOptions<schema.DatasetGroupsQuery, schema.DatasetGroupsQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.DatasetGroupsQuery, schema.DatasetGroupsQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.DatasetGroupsQuery, schema.DatasetGroupsQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.DatasetGroupsQuery, schema.DatasetGroupsQueryVariables>(DatasetGroupsDocument, variables, options);
}
export type DatasetGroupsQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.DatasetGroupsQuery, schema.DatasetGroupsQueryVariables>;
export const DatasetGroupDocument = gql`
    query datasetGroup($id: UUID!) {
  datasetGroup(id: $id) {
    ...DatasetGroupFullyFragment
  }
}
    ${DatasetGroupFullyFragmentFragmentDoc}`;

/**
 * __useDatasetGroupQuery__
 *
 * To run a query within a Vue component, call `useDatasetGroupQuery` and pass it any options that fit your needs.
 * When your component renders, `useDatasetGroupQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useDatasetGroupQuery({
 *   id: // value for 'id'
 * });
 */
export function useDatasetGroupQuery(variables: schema.DatasetGroupQueryVariables | VueCompositionApi.Ref<schema.DatasetGroupQueryVariables> | ReactiveFunction<schema.DatasetGroupQueryVariables>, options: VueApolloComposable.UseQueryOptions<schema.DatasetGroupQuery, schema.DatasetGroupQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.DatasetGroupQuery, schema.DatasetGroupQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.DatasetGroupQuery, schema.DatasetGroupQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.DatasetGroupQuery, schema.DatasetGroupQueryVariables>(DatasetGroupDocument, variables, options);
}
export type DatasetGroupQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.DatasetGroupQuery, schema.DatasetGroupQueryVariables>;
export const SimilarDatasetsDocument = gql`
    query similarDatasets($datasetGroupId: String!, $keyword: String) {
  similarDatasets(datasetGroupId: $datasetGroupId, keyword: $keyword) {
    sim
    datasetGroup {
      id
      name
      source {
        siteName
        siteUrl
      }
      originalFile
      createdBy
      createdAt
      currentDataset {
        numRecords
        numColumns
        analyzedStatus
        isAnalyzed
        hasAnnotates
        fileSize
        filterJson
        attrNames
        dataFile
        version
        createdAt
        attrs {
          id
          index
          name
        }
      }
    }
  }
}
    `;

/**
 * __useSimilarDatasetsQuery__
 *
 * To run a query within a Vue component, call `useSimilarDatasetsQuery` and pass it any options that fit your needs.
 * When your component renders, `useSimilarDatasetsQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useSimilarDatasetsQuery({
 *   datasetGroupId: // value for 'datasetGroupId'
 *   keyword: // value for 'keyword'
 * });
 */
export function useSimilarDatasetsQuery(variables: schema.SimilarDatasetsQueryVariables | VueCompositionApi.Ref<schema.SimilarDatasetsQueryVariables> | ReactiveFunction<schema.SimilarDatasetsQueryVariables>, options: VueApolloComposable.UseQueryOptions<schema.SimilarDatasetsQuery, schema.SimilarDatasetsQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.SimilarDatasetsQuery, schema.SimilarDatasetsQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.SimilarDatasetsQuery, schema.SimilarDatasetsQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.SimilarDatasetsQuery, schema.SimilarDatasetsQueryVariables>(SimilarDatasetsDocument, variables, options);
}
export type SimilarDatasetsQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.SimilarDatasetsQuery, schema.SimilarDatasetsQueryVariables>;
export const GetDatasetDocument = gql`
    query GetDataset($id: UUID!) {
  dataset(id: $id) {
    ...DatasetFragment
  }
}
    ${DatasetFragmentFragmentDoc}`;

/**
 * __useGetDatasetQuery__
 *
 * To run a query within a Vue component, call `useGetDatasetQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetDatasetQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useGetDatasetQuery({
 *   id: // value for 'id'
 * });
 */
export function useGetDatasetQuery(variables: schema.GetDatasetQueryVariables | VueCompositionApi.Ref<schema.GetDatasetQueryVariables> | ReactiveFunction<schema.GetDatasetQueryVariables>, options: VueApolloComposable.UseQueryOptions<schema.GetDatasetQuery, schema.GetDatasetQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.GetDatasetQuery, schema.GetDatasetQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.GetDatasetQuery, schema.GetDatasetQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.GetDatasetQuery, schema.GetDatasetQueryVariables>(GetDatasetDocument, variables, options);
}
export type GetDatasetQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.GetDatasetQuery, schema.GetDatasetQueryVariables>;
export const OwnDatasetGroupsDocument = gql`
    query ownDatasetGroups($keyword: String, $page: Int, $pageSize: Int) {
  ownDatasetGroups(keyword: $keyword, page: $page, pageSize: $pageSize) {
    keyword
    page
    pageSize
    totalRecords
    datasetGroups {
      ...DatasetGroupFragment
    }
  }
}
    ${DatasetGroupFragmentFragmentDoc}`;

/**
 * __useOwnDatasetGroupsQuery__
 *
 * To run a query within a Vue component, call `useOwnDatasetGroupsQuery` and pass it any options that fit your needs.
 * When your component renders, `useOwnDatasetGroupsQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useOwnDatasetGroupsQuery({
 *   keyword: // value for 'keyword'
 *   page: // value for 'page'
 *   pageSize: // value for 'pageSize'
 * });
 */
export function useOwnDatasetGroupsQuery(variables: schema.OwnDatasetGroupsQueryVariables | VueCompositionApi.Ref<schema.OwnDatasetGroupsQueryVariables> | ReactiveFunction<schema.OwnDatasetGroupsQueryVariables> = {}, options: VueApolloComposable.UseQueryOptions<schema.OwnDatasetGroupsQuery, schema.OwnDatasetGroupsQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.OwnDatasetGroupsQuery, schema.OwnDatasetGroupsQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.OwnDatasetGroupsQuery, schema.OwnDatasetGroupsQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.OwnDatasetGroupsQuery, schema.OwnDatasetGroupsQueryVariables>(OwnDatasetGroupsDocument, variables, options);
}
export type OwnDatasetGroupsQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.OwnDatasetGroupsQuery, schema.OwnDatasetGroupsQueryVariables>;
export const GetOwnUserDocument = gql`
    query GetOwnUser {
  ownUser {
    name
    email
  }
}
    `;

/**
 * __useGetOwnUserQuery__
 *
 * To run a query within a Vue component, call `useGetOwnUserQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetOwnUserQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useGetOwnUserQuery();
 */
export function useGetOwnUserQuery(options: VueApolloComposable.UseQueryOptions<schema.GetOwnUserQuery, schema.GetOwnUserQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.GetOwnUserQuery, schema.GetOwnUserQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.GetOwnUserQuery, schema.GetOwnUserQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.GetOwnUserQuery, schema.GetOwnUserQueryVariables>(GetOwnUserDocument, {}, options);
}
export type GetOwnUserQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.GetOwnUserQuery, schema.GetOwnUserQueryVariables>;
export const GetManySuggestsByDatasetGroupDocument = gql`
    query getManySuggestsByDatasetGroup($datasetGroupId: UUID!, $targetDatasetGroupId: UUID) {
  suggestByDatasetGroup(
    datasetGroupId: $datasetGroupId
    targetDatasetGroupId: $targetDatasetGroupId
  ) {
    datasetGroup {
      ...DatasetGroupFullyFragment
    }
    targetDatasetGroup {
      ...DatasetGroupFullyFragment
    }
    suggests {
      sourceIndex
      title
      message
      filterKey
      filterParams
    }
  }
}
    ${DatasetGroupFullyFragmentFragmentDoc}`;

/**
 * __useGetManySuggestsByDatasetGroupQuery__
 *
 * To run a query within a Vue component, call `useGetManySuggestsByDatasetGroupQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetManySuggestsByDatasetGroupQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useGetManySuggestsByDatasetGroupQuery({
 *   datasetGroupId: // value for 'datasetGroupId'
 *   targetDatasetGroupId: // value for 'targetDatasetGroupId'
 * });
 */
export function useGetManySuggestsByDatasetGroupQuery(variables: schema.GetManySuggestsByDatasetGroupQueryVariables | VueCompositionApi.Ref<schema.GetManySuggestsByDatasetGroupQueryVariables> | ReactiveFunction<schema.GetManySuggestsByDatasetGroupQueryVariables>, options: VueApolloComposable.UseQueryOptions<schema.GetManySuggestsByDatasetGroupQuery, schema.GetManySuggestsByDatasetGroupQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.GetManySuggestsByDatasetGroupQuery, schema.GetManySuggestsByDatasetGroupQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.GetManySuggestsByDatasetGroupQuery, schema.GetManySuggestsByDatasetGroupQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.GetManySuggestsByDatasetGroupQuery, schema.GetManySuggestsByDatasetGroupQueryVariables>(GetManySuggestsByDatasetGroupDocument, variables, options);
}
export type GetManySuggestsByDatasetGroupQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.GetManySuggestsByDatasetGroupQuery, schema.GetManySuggestsByDatasetGroupQueryVariables>;
export const GetManySuggestsByDatasetTemplateDocument = gql`
    query getManySuggestsByDatasetTemplate($datasetGroupId: UUID!, $targetDatasetTemplateId: UUID) {
  suggestByDatasetTemplate(
    datasetGroupId: $datasetGroupId
    targetDatasetTemplateId: $targetDatasetTemplateId
  ) {
    datasetGroup {
      ...DatasetGroupFullyFragment
    }
    targetDatasetTemplate {
      ...DatasetTemplateFragment
    }
    suggests {
      sourceIndex
      title
      message
      filterKey
      filterParams
    }
  }
}
    ${DatasetGroupFullyFragmentFragmentDoc}
${DatasetTemplateFragmentFragmentDoc}`;

/**
 * __useGetManySuggestsByDatasetTemplateQuery__
 *
 * To run a query within a Vue component, call `useGetManySuggestsByDatasetTemplateQuery` and pass it any options that fit your needs.
 * When your component renders, `useGetManySuggestsByDatasetTemplateQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useGetManySuggestsByDatasetTemplateQuery({
 *   datasetGroupId: // value for 'datasetGroupId'
 *   targetDatasetTemplateId: // value for 'targetDatasetTemplateId'
 * });
 */
export function useGetManySuggestsByDatasetTemplateQuery(variables: schema.GetManySuggestsByDatasetTemplateQueryVariables | VueCompositionApi.Ref<schema.GetManySuggestsByDatasetTemplateQueryVariables> | ReactiveFunction<schema.GetManySuggestsByDatasetTemplateQueryVariables>, options: VueApolloComposable.UseQueryOptions<schema.GetManySuggestsByDatasetTemplateQuery, schema.GetManySuggestsByDatasetTemplateQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.GetManySuggestsByDatasetTemplateQuery, schema.GetManySuggestsByDatasetTemplateQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.GetManySuggestsByDatasetTemplateQuery, schema.GetManySuggestsByDatasetTemplateQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.GetManySuggestsByDatasetTemplateQuery, schema.GetManySuggestsByDatasetTemplateQueryVariables>(GetManySuggestsByDatasetTemplateDocument, variables, options);
}
export type GetManySuggestsByDatasetTemplateQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.GetManySuggestsByDatasetTemplateQuery, schema.GetManySuggestsByDatasetTemplateQueryVariables>;
export const TemplatesDocument = gql`
    query templates($keyword: String) {
  templates(keyword: $keyword) {
    id
    name
    desc
    attrs {
      id
      name
    }
  }
}
    `;

/**
 * __useTemplatesQuery__
 *
 * To run a query within a Vue component, call `useTemplatesQuery` and pass it any options that fit your needs.
 * When your component renders, `useTemplatesQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param variables that will be passed into the query
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useTemplatesQuery({
 *   keyword: // value for 'keyword'
 * });
 */
export function useTemplatesQuery(variables: schema.TemplatesQueryVariables | VueCompositionApi.Ref<schema.TemplatesQueryVariables> | ReactiveFunction<schema.TemplatesQueryVariables> = {}, options: VueApolloComposable.UseQueryOptions<schema.TemplatesQuery, schema.TemplatesQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.TemplatesQuery, schema.TemplatesQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.TemplatesQuery, schema.TemplatesQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.TemplatesQuery, schema.TemplatesQueryVariables>(TemplatesDocument, variables, options);
}
export type TemplatesQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.TemplatesQuery, schema.TemplatesQueryVariables>;
export const OwnUserDocument = gql`
    query ownUser {
  ownUser {
    id
    name
    email
  }
}
    `;

/**
 * __useOwnUserQuery__
 *
 * To run a query within a Vue component, call `useOwnUserQuery` and pass it any options that fit your needs.
 * When your component renders, `useOwnUserQuery` returns an object from Apollo Client that contains result, loading and error properties
 * you can use to render your UI.
 *
 * @param options that will be passed into the query, supported options are listed on: https://v4.apollo.vuejs.org/guide-composable/query.html#options;
 *
 * @example
 * const { result, loading, error } = useOwnUserQuery();
 */
export function useOwnUserQuery(options: VueApolloComposable.UseQueryOptions<schema.OwnUserQuery, schema.OwnUserQueryVariables> | VueCompositionApi.Ref<VueApolloComposable.UseQueryOptions<schema.OwnUserQuery, schema.OwnUserQueryVariables>> | ReactiveFunction<VueApolloComposable.UseQueryOptions<schema.OwnUserQuery, schema.OwnUserQueryVariables>> = {}) {
  return VueApolloComposable.useQuery<schema.OwnUserQuery, schema.OwnUserQueryVariables>(OwnUserDocument, {}, options);
}
export type OwnUserQueryCompositionFunctionResult = VueApolloComposable.UseQueryReturn<schema.OwnUserQuery, schema.OwnUserQueryVariables>;